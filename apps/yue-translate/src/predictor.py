import json
import os

import flask
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from translator import Translator
from translation_pipeline import TranslationPipeline

prefix = "/opt/ml/"
model_path = "hon9kon9ize/bart-translation-zh-yue-onnx"

# The flask app for serving predictions
app = flask.Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = ORTModelForSeq2SeqLM.from_pretrained(
    model_path,
    provider="CPUExecutionProvider",
    encoder_file_name="encoder_model_quantized.onnx",
    decoder_file_name="decoder_model_quantized.onnx",
    decoder_file_with_past_name="decoder_with_past_model_quantized.onnx",
)
pipe = TranslationPipeline(model, tokenizer, do_sample=False, num_beams=1)
translator = Translator(pipe, max_length=512, batch_size=1)


@app.route("/ping", methods=["GET"])
def ping():
    return flask.Response(response="\n", status=200, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def invocations():
    # Process input
    input_json = flask.request.get_json()
    print(input_json)
    data = input_json["input"]

    if len(data) == 0:
        return flask.Response(
            response="No input text provided", status=400, mimetype="text/plain"
        )

    # Custom model
    result = translator(data)[0]

    print(result)

    # Return value
    result = json.dumps({"output": result}, ensure_ascii=False)
    return flask.Response(response=result, status=200, mimetype="application/json")
