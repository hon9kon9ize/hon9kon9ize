from collections.abc import Callable
import traceback
from typing import List, Union
from datasets import Dataset
import re
import pickle
import os
from transformers.pipelines.pt_utils import KeyDataset
from transformers import AutoTokenizer
from tqdm.auto import tqdm

URL_REGEX = re.compile(r"\b(https?://\S+)\b")
EMAIL_REGEX = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
TAG_REGEX = re.compile(r"<[^>]+>")
HANDLE_REGEX = re.compile(r"[^a-zA-Z](@\w+)")
CHINESE_CHAR_RANGE = re.compile(
    r"[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002ebef\U00030000-\U000323af\ufa0e\ufa0f\ufa11\ufa13\ufa14\ufa1f\ufa21\ufa23\ufa24\ufa27\ufa28\ufa29\u3006\u3007][\ufe00-\ufe0f\U000e0100-\U000e01ef]?")


class Translator:
    def __init__(
        self,
        pipe: Callable,
        max_length: int = 500,
        batch_size: int = 16,
        save_every_step=100,
        text_key="text",
        save_filename=None,
        replace_chinese_puncts=False,
        verbose=False,
    ):
        self.pipe = pipe
        self.max_length = max_length
        self.batch_size = batch_size
        self.save_every_step = save_every_step
        self.save_filename = save_filename
        self.text_key = text_key
        self.replace_chinese_puncts = replace_chinese_puncts
        self.verbose = verbose

        if max_length == None and hasattr(pipe.model.config, "max_length"):
            self.max_length = pipe.model.config.max_length

    def _is_chinese(self, text: str) -> bool:
        return CHINESE_CHAR_RANGE.search(text) is not None

    def _split_sentences(self, text: str) -> List[str]:
        tokens = self.pipe.tokenizer(text, add_special_tokens=False)
        token_size = len(tokens.input_ids)

        if len(text) <= self.max_length:
            return [text]

        delimiter = set()
        delimiter.update("。！？；…!?;")
        sent_list = []
        sent = text

        while token_size > self.max_length:
            orig_sent_len = token_size

            # find the index of delimiter near the max_length
            for i in range(token_size - 2, 0, -1):
                token = tokens.token_to_chars(0, i)
                char = sent[token.start:token.end]

                if char in delimiter:
                    split_char_index = token.end
                    next_sent = sent[split_char_index:]

                    if len(next_sent) == 1:
                        continue

                    sent_list = [next_sent] + sent_list
                    sent = sent[0:split_char_index]
                    break

            tokens = self.pipe.tokenizer(
                sent, add_special_tokens=False)
            token_size = len(tokens.input_ids)

            # no delimiter found, leave the sentence as it is
            if token_size == orig_sent_len:
                sent_list = [sent] + sent_list
                sent = ""
                break

        if len(sent) > 0:
            sent_list = [sent] + sent_list

        return sent_list

    def _preprocess(self, text: str) -> (str, str):
        # extract entities
        tags = TAG_REGEX.findall(text)
        handles = HANDLE_REGEX.findall(text)
        urls = URL_REGEX.findall(text)
        emails = EMAIL_REGEX.findall(text)
        entities = urls + emails + tags + handles

        # TODO: escape entity placeholders

        for i, entity in enumerate(entities):
            text = text.replace(entity, "¡%d¡" % i, 1)

        lines = text.split("\n")
        sentences = []
        num_tokens = []
        template = text.replace("{", "{{").replace("}", "}}")
        chunk_index = 0

        for line in lines:
            sentence = line.strip()

            if len(sentence) > 0 and self._is_chinese(sentence):
                chunks = self._split_sentences(sentence)

                for chunk in chunks:
                    sentences.append(chunk)
                    tokens = self.pipe.tokenizer(
                        chunk, add_special_tokens=False)
                    num_tokens.append(len(tokens.input_ids))
                    chunk = chunk.replace("{", "{{").replace("}", "}}")
                    template = template.replace(
                        chunk, "{%d}" % chunk_index, 1)
                    chunk_index += 1

        return sentences, template, num_tokens, entities

    def _postprocess(
        self, template: str, src_sentences: List[str], translations: List[str], entities: List[str]
    ) -> str:
        processed = []
        alphanumeric_regex = re.compile(
            "([a-zA-Zａ-ｚＡ-Ｚ０-９\d+'\",，（\(）\)：:；;“”。·\.\？?\！!‘’$\[\]<>/\s]+)"
        )

        def hash_text(text: List[str]) -> str:
            text = "|".join(text)
            puncts_map = str.maketrans("，；：（）。？！“”‘’", ",;:().?!\"\"''")
            text = text.translate(puncts_map)
            return text.lower()

        for i, p in enumerate(translations):
            src_sentence = src_sentences[i]

            if self.replace_chinese_puncts:
                p = re.sub(',', '，', p)  # replace all commas
                p = re.sub(';', '；', p)  # replace semi-colon
                p = re.sub(':', '：', p)  # replace colon
                p = re.sub('\(', '（', p)  # replace round basket
                p = re.sub('\)', '）', p)  # replace round basket
                p = re.sub(r'([\d])，([\d])', r'\1,\2', p)

            src_matches = re.findall(alphanumeric_regex, src_sentence)
            tgt_matches = re.findall(alphanumeric_regex, p)

            # length not match or no match
            if (
                len(src_matches) != len(tgt_matches)
                or len(src_matches) == 0
                or len(tgt_matches) == 0
            ):
                processed.append(p)
                continue

            # normalize full-width to half-width and lower case
            src_hashes = hash_text(src_matches)
            translated_hashes = hash_text(tgt_matches)

            if src_hashes != translated_hashes:
                # fix unmatched
                for j in range(len(src_matches)):
                    if src_matches[j] != tgt_matches[j]:
                        p = p.replace(tgt_matches[j], src_matches[j], 1)
            elif ''.join(src_matches) != ''.join(tgt_matches):
                p_blanks = re.split('|'.join(tgt_matches), p)
                # fill blank with src matches
                for j in range(len(src_matches)):
                    p_blanks[j] = p_blanks[j] + src_matches[j]

                p = "".join(p_blanks)
                print(p)

            processed.append(p)

        output = template.format(*processed)

        # replace entities
        for i, entity in enumerate(entities):
            output = output.replace("¡%d¡" % i, entity, 1)

        # TODO: unescape entity placeholders

        # fix repeated punctuations
        output = re.sub(r'([「」（）『』《》。，：])\1+', r'\1', output)

        # fix brackets
        if '“' in output:
            output = re.sub('“', '「', output)
        if '”' in output:
            output = re.sub('”', '」', output)

        return output

    def _save(self, translations):
        with open(self.save_filename, "wb") as f:
            pickle.dump(translations, f)

    def __call__(self, inputs: Union[List[str], Dataset]) -> List[str]:
        templates = []
        sentences = []
        num_tokens = []
        sentence_indices = []
        outputs = []
        translations = []
        entities_list = []
        resume_from_file = None

        if isinstance(inputs, Dataset):
            ds = inputs
        else:
            if isinstance(inputs, str):
                inputs = [inputs]
            ds = Dataset.from_list([{"text": text} for text in inputs])

        for i, text_input in tqdm(enumerate(ds), total=len(ds), desc="Preprocessing", disable=not self.verbose):
            chunks, template, my_num_tokens, entities = self._preprocess(
                text_input["text"])
            templates.append(template)
            sentence_indices.append([])
            entities_list.append(entities)

            for j, chunk in enumerate(chunks):
                sentences.append(chunk)
                sentence_indices[len(sentence_indices) -
                                 1].append(len(sentences) - 1)
                num_tokens.append(my_num_tokens[j])

        if self.save_filename:
            resume_from_file = (
                self.save_filename
                if os.path.isfile(self.save_filename)
                else None
            )

        if resume_from_file != None:
            translations = pickle.load(open(resume_from_file, "rb"))

        if self.verbose:
            print("translated:", len(translations))
            print("to translate:", len(sentences) - len(translations))

            if resume_from_file != None:
                print("Resuming from {}({} records)".format(
                    resume_from_file, len(translations)))

        ds = Dataset.from_list(
            [{"text": text} for text in sentences[len(translations):]]
        )

        max_token_length = max(num_tokens) if len(num_tokens) > 0 else 0

        if self.verbose:
            print('Max Length:', max_token_length)

        total_records = len(ds)

        if total_records > 0:
            step = 0

            with tqdm(disable=not self.verbose, desc="Translating", total=total_records) as pbar:
                for out in self.pipe(
                    KeyDataset(ds, self.text_key), batch_size=self.batch_size, max_length=self.max_length
                ):
                    translations.append(out[0])

                    # export generate result every n steps
                    if (
                        step != 0
                        and self.save_filename != None
                        and step % self.save_every_step == 0
                    ):
                        self._save(translations)

                    step += 1

                    pbar.update(1)

        if self.save_filename != None and total_records > 0:
            self._save(translations)

        for i, template in tqdm(enumerate(templates), total=len(templates), desc="Postprocessing", disable=not self.verbose):
            try:
                src_sentences = [sentences[index]
                                 for index in sentence_indices[i]]
                tgt_sentences = [
                    translations[index]["translation_text"]
                    for index in sentence_indices[i]
                ]
                output = self._postprocess(
                    template, src_sentences, tgt_sentences, entities_list[i]
                )
                outputs.append(output)
            except Exception as error:
                print(error)
                print(template)
                traceback.print_exc()
                # print(template, sentence_indices[i], len(translations))

        return outputs


class Object(object):
    pass


class FakePipe(object):
    def __init__(self, max_length: int = 500):
        self.model = Object()
        self.model.config = Object()
        self.model.config.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(
            'indiejoseph/bart-translation-zh-yue')

    def __call__(self, text: List[str], batch_size: str, max_length: int):
        for i in range(len(text)):
            sentence = text[i]
            # extract entities
            tags = re.findall(TAG_REGEX, sentence)
            handles = re.findall(HANDLE_REGEX, sentence)
            urls = re.findall(URL_REGEX, sentence)
            emails = re.findall(EMAIL_REGEX, sentence)
            entities = urls + emails + tags + handles

            for i, entity in enumerate(entities):
                sentence = sentence.replace(entity, "¡[%d]¡" % i, 1)

            if "１２３" in sentence:
                yield [{"translation_text": sentence.replace("１２３", "123")}]
                continue
            if "abc" in sentence:
                yield [{"translation_text": sentence.replace("abc", "ABC")}]
                continue
            if "Acetaminophen" in sentence:
                yield [{"translation_text": sentence.replace("Acetaminophen", "ACEtaminidien")}]
                continue
            if re.search('\d+\.\s', sentence):
                yield [{"translation_text": sentence.replace(r'(\d+\.)\s', r'\1')}]
                continue
            yield [{"translation_text": sentence}]


if __name__ == "__main__":
    fake_pipe = FakePipe(60)

    translator = Translator(fake_pipe, max_length=60,
                            batch_size=2, verbose=True)

    text1 = "对于编写聊天机器人的脚本，你可以采用不同的方法，包括使用基于规则的系统、自然语言处理（NLP）技术和机器学习模型。下面是一个简单的例子，展示如何使用基于规则的方法来构建一个简单的聊天机器人："
    text2 = """对于编写聊天机器人的脚本，你可以采用不同的方法，包括使用基于规则的系统、自然语言处理（NLP）技术和机器学习模型。下面是一个简单的例子，展示如何使用基于规则的方法来构建一个简单的聊天机器人：

```
# 设置用于匹配输入的关键字，并定义相应的回答数据字典。
keywords = {'你好': '你好！很高兴见到你。',
           '再见': '再见！有机会再聊。',
           '你叫什么': '我是一个聊天机器人。',
           '你是谁': '我是一个基于人工智能技术制作的聊天机器人。'}

# 定义用于处理用户输入的函数。
def chatbot(input_text):
    # 遍历关键字数据字典，匹配用户的输入。
    for key in keywords:
        if key in input_text:
            # 如果匹配到了关键字，返回相应的回答。
            return keywords[key]
    # 如果没有找到匹配的关键字，返回默认回答。
    return "对不起，我不知道你在说什么。"

# 运行聊天机器人。
while True:
    # 获取用户输入。
    user_input = input('用户: ')
    # 如果用户输入“再见”，退出程序。
    if user_input == '再见':
        break
    # 处理用户输入，并打印回答。
    print('机器人: ' + chatbot(user_input))
```

这是一个非常简单的例子。对于实用的聊天机器人，可能需要使用更复杂的 NLP 技术和机器学习模型，以更好地理解和回答用户的问题。"""
    text3 = "布洛芬(Ibuprofen)同撲熱息痛(Acetaminophen)係兩種常見嘅非處方藥，用於緩解疼痛、發燒同關節痛。"
    text4 = "１２３ “abc” def's http://www.google.com abc@abc.com @abc 網址：http://localhost/abc下載"
    text5 = "新力公司董事長盛田昭夫、自民黨國會議員石原慎太郎等人撰寫嘅《日本可以說「不」》、《日本還要說「不」》、《日本堅決說「不」》三本書中話道：「無啦啦挑起戰爭嘅好戰日本人，製造南京大屠殺嘅殘暴嘅日本人，呢d就係人地對日本人嘅兩個誤解，都係‘敲打日本’嘅兩個根由，我地必須採取措施消除佢。」"
    text6 = "List:\n1. abc\n2. xyz"
    text7 = "例子。<mask>"
    outputs = translator([text1, text2, text3, text4, text5, text6, text7])

    # for i, line in enumerate(outputs[1].split("\n")):
    #     input_text = text2.split("\n")[i]

    #     if line != input_text:
    #         print(line, text2.split("\n")[i])

    assert outputs[0] == text1
    assert outputs[1] == text2.replace("“", "「").replace("”", "」")
    assert outputs[2] == text3
    assert outputs[3] == text4.replace("“", "「").replace("”", "」")
    assert outputs[4] == text5
    assert outputs[5] == text6
    assert outputs[6] == text7

    # exception
    assert len(translator._split_sentences(
        "新力公司董事長盛田昭夫、自民黨國會議員石原慎太郎等人撰寫嘅《日本可以說「不」》、《日本還要說「不」》、《日本堅決說「不」》三本書中話道：「無啦啦挑起戰爭嘅好戰日本人，製造南京大屠殺嘅殘暴嘅日本人，呢d就係人地對日本人嘅兩個誤解，都係‘敲打日本’嘅兩個根由，我地必須採取措施消除佢。」")) == 1

    translator = Translator(fake_pipe, max_length=5,
                            batch_size=2, verbose=True)

    assert len(translator._split_sentences(
        "====。====。====。====。====。====。====。====。====。")) == 9

    # test non-chinese
    outputs = translator(["abc", "123"])

    assert outputs[0] == "abc"
    assert outputs[1] == "123"

    # test _postprocess
    assert translator._postprocess(
        "{}", ["abc"], ["ABC"], []) == "abc"

    print(translator._postprocess(
        "{}\n{}", ["($1,000)", "XYZ"], ["( $1, 000 )", "xyz"], []))

    assert translator._postprocess(
        "{}\n{}", ["($1,000)", "XYZ"], ["( $1, 000 )", "xyz"], []) == "($1,000)\nXYZ"
