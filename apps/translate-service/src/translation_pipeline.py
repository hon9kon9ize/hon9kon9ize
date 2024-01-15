from transformers import TranslationPipeline as HfTranslationPipeline
from transformers.pipelines.text2text_generation import ReturnType
import re


hans_chars = set(
    "万与专业丛东丝丢两严丧个丬丰临为丽举么义乌乐乔习乡书买乱争于亏亘亚产亩亲亵亸亿仅从仑仓仪们价众优会伛伞伟传伤伥伦伧伪伫体佥侠侣侥侦侧侨侩侪侬俣俦俨俩俪俭债倾偬偻偾偿傥傧储傩儿兑兖党兰关兴兹养兽冁内冈册写军农冢冯冲决况冻净凄凉减凑凛凤凫凭凯击凼凿刍刘则刚创删别刬刭刽刿剀剂剐剑剥剧劝办务劢动励劲劳势勋勐勚匀匦匮区医华协单卖卢卤卫却卺厂厅历厉压厌厍厕厢厣厦厨厩厮县参叆叇双发变叙叠叶号叹叽吁吕吗吣吨听启吴呒呓呕呖呗员呙呛呜咏咙咛咝咤咴哌哑哒哓哔哕哗哙哜哝哟唛唝唠唡唢唣唤唿啧啬啭啮啰啴啸喷喽喾嗫嗳嘘嘤嘱噜嚣嚯团园囱围囵国图圆圣圹场坂坏块坚坛坜坝坞坟坠垄垅垆垒垦垧垩垫垭垯垱垲垴埘埙埚埝埯堑堕塆墙壮声壳壶壸处备复够头夸夹夺奁奂奋奖奥妆妇妈妩妪妫姗娄娅娆娇娈娱娲娴婳婴婵婶媪嫒嫔嫱嬷孙学孪宁宝实宠审宪宫宽宾寝对寻导寿将尔尘尧尴尸尽层屃屉届属屡屦屿岁岂岖岗岘岙岚岛岭岽岿峃峄峡峣峤峥峦崂崃崄崭嵘嵚嵛嵝嵴巅巩巯币帅师帏帐帘帜带帧帮帱帻帼幂幞并广庄庆庐庑库应庙庞废庼廪开异弃张弥弪弯弹强归当录彟彦彻径徕忆忏忧忾怀态怂怃怄怅怆怜总怼怿恋恳恶恸恹恺恻恼恽悦悫悬悭悯惊惧惨惩惫惬惭惮惯愍愠愤愦愿慑慭憷懑懒懔戆戋戏戗战戬户扦执扩扪扫扬扰抚抛抟抠抡抢护报担拟拢拣拥拦拧拨择挂挚挛挜挝挞挟挠挡挢挣挤挥挦捞损捡换捣据掳掴掷掸掺掼揽揿搀搁搂搅携摄摅摆摇摈摊撄撵撷撸撺擞攒敌敛数斋斓斩断无旧时旷旸昙昼昽显晋晒晓晔晕晖暂暧术机杀杂权条来杨杩极构枞枢枣枥枧枨枪枫枭柜柠柽栀栅标栈栉栊栋栌栎栏树栖样栾桊桠桡桢档桤桥桦桧桨桩梦梼梾检棂椁椟椠椤椭楼榄榇榈榉槚槛槟槠横樯樱橥橱橹橼檩欢欤欧歼殁殇残殒殓殚殡殴毁毂毕毙毡毵氇气氢氩氲汇汉汤汹沓沟没沣沤沥沦沧沨沩沪沵泞泪泶泷泸泺泻泼泽泾洁洒洼浃浅浆浇浈浉浊测浍济浏浐浑浒浓浔浕涛涝涞涟涠涡涢涣涤润涧涨涩淀渊渌渍渎渐渑渔渖渗温湾湿溃溅溆溇滗滚滞滟滠满滢滤滥滦滨滩滪漤潆潇潋潍潜潴澜濑濒灏灭灯灵灾灿炀炉炖炜炝点炼炽烁烂烃烛烟烦烧烨烩烫烬热焕焖焘煅煳熘爱爷牍牦牵牺犊犟状犷犸犹狈狍狝狞独狭狮狯狰狱狲猃猎猕猡猪猫猬献獭玑玙玚玛玮环现玱玺珉珏珐珑珰珲琎琏琐琼瑶瑷璎瓒瓮瓯电画畅畲畴疖疗疟疠疡疬疮疯疴痈痉痒痖痨痪痫瘅瘆瘗瘘瘪瘫瘾瘿癞癣癫癯皑皱皲盏盐监盖盗盘眍眦眬睁睐睑瞒瞩矫矶矾矿砀码砖砗砚砜砺砻砾础硁硕硖硗硙硚确硷碍碛碜碱碹磙礼祎祢祯祷祸禀禄禅离秃秆种积称秽秾稆税稣稳穑穷窃窍窑窜窝窥窦窭竖竞笃笋笔笕笺笼笾筑筚筛筜筝筹签简箓箦箧箨箩箪箫篑篓篮篱簖籁籴类籼粜粝粤粪粮糁糇紧絷纟纠纡红纣纤纥约级纨纩纪纫纬纭纮纯纰纱纲纳纴纵纶纷纸纹纺纻纼纽纾线绀绁绂练组绅细织终绉绊绋绌绍绎经绐绑绒结绔绕绖绗绘给绚绛络绝绞统绠绡绢绣绤绥绦继绨绩绪绫绬续绮绯绰绱绲绳维绵绶绷绸绹绺绻综绽绾绿缀缁缂缃缄缅缆缇缈缉缊缋缌缍缎缏缐缑缒缓缔缕编缗缘缙缚缛缜缝缞缟缠缡缢缣缤缥缦缧缨缩缪缫缬缭缮缯缰缱缲缳缴缵罂网罗罚罢罴羁羟羡翘翙翚耢耧耸耻聂聋职聍联聩聪肃肠肤肷肾肿胀胁胆胜胧胨胪胫胶脉脍脏脐脑脓脔脚脱脶脸腊腌腘腭腻腼腽腾膑臜舆舣舰舱舻艰艳艹艺节芈芗芜芦苁苇苈苋苌苍苎苏苘苹茎茏茑茔茕茧荆荐荙荚荛荜荞荟荠荡荣荤荥荦荧荨荩荪荫荬荭荮药莅莜莱莲莳莴莶获莸莹莺莼萚萝萤营萦萧萨葱蒇蒉蒋蒌蓝蓟蓠蓣蓥蓦蔷蔹蔺蔼蕲蕴薮藁藓虏虑虚虫虬虮虽虾虿蚀蚁蚂蚕蚝蚬蛊蛎蛏蛮蛰蛱蛲蛳蛴蜕蜗蜡蝇蝈蝉蝎蝼蝾螀螨蟏衅衔补衬衮袄袅袆袜袭袯装裆裈裢裣裤裥褛褴襁襕见观觃规觅视觇览觉觊觋觌觍觎觏觐觑觞触觯詟誉誊讠计订讣认讥讦讧讨让讪讫训议讯记讱讲讳讴讵讶讷许讹论讻讼讽设访诀证诂诃评诅识诇诈诉诊诋诌词诎诏诐译诒诓诔试诖诗诘诙诚诛诜话诞诟诠诡询诣诤该详诧诨诩诪诫诬语诮误诰诱诲诳说诵诶请诸诹诺读诼诽课诿谀谁谂调谄谅谆谇谈谊谋谌谍谎谏谐谑谒谓谔谕谖谗谘谙谚谛谜谝谞谟谠谡谢谣谤谥谦谧谨谩谪谫谬谭谮谯谰谱谲谳谴谵谶豮贝贞负贠贡财责贤败账货质贩贪贫贬购贮贯贰贱贲贳贴贵贶贷贸费贺贻贼贽贾贿赀赁赂赃资赅赆赇赈赉赊赋赌赍赎赏赐赑赒赓赔赕赖赗赘赙赚赛赜赝赞赟赠赡赢赣赪赵赶趋趱趸跃跄跖跞践跶跷跸跹跻踊踌踪踬踯蹑蹒蹰蹿躏躜躯车轧轨轩轪轫转轭轮软轰轱轲轳轴轵轶轷轸轹轺轻轼载轾轿辀辁辂较辄辅辆辇辈辉辊辋辌辍辎辏辐辑辒输辔辕辖辗辘辙辚辞辩辫边辽达迁过迈运还这进远违连迟迩迳迹适选逊递逦逻遗遥邓邝邬邮邹邺邻郄郏郐郑郓郦郧郸酝酦酱酽酾酿释鉴銮錾钆钇针钉钊钋钌钍钎钏钐钑钒钓钔钕钖钗钘钙钚钛钝钞钟钠钡钢钣钤钥钦钧钨钩钪钫钬钭钮钯钰钱钲钳钴钵钶钷钸钹钺钻钼钽钾钿铀铁铂铃铄铅铆铈铉铊铋铍铎铏铐铑铒铕铗铘铙铚铛铜铝铞铟铠铡铢铣铤铥铦铧铨铪铫铬铭铮铯铰铱铲铳铴铵银铷铸铹铺铻铼铽链铿销锁锂锃锄锅锆锇锈锉锊锋锌锍锎锏锐锑锒锓锔锕锖锗错锚锜锞锟锠锡锢锣锤锥锦锨锩锫锬锭键锯锰锱锲锳锴锵锶锷锸锹锺锻锼锽锾锿镀镁镂镃镆镇镈镉镊镌镍镎镏镐镑镒镕镖镗镙镚镛镜镝镞镟镠镡镢镣镤镥镦镧镨镩镪镫镬镭镮镯镰镱镲镳镴镶长门闩闪闫闬闭问闯闰闱闲闳间闵闶闷闸闹闺闻闼闽闾闿阀阁阂阃阄阅阆阇阈阉阊阋阌阍阎阏阐阑阒阓阔阕阖阗阘阙阚阛队阳阴阵阶际陆陇陈陉陕陧陨险随隐隶隽难雏雠雳雾霁霭靓静靥鞑鞒鞯鞴韦韧韨韩韪韫韬韵页顶顷顸项顺须顼顽顾顿颀颁颂颃预颅领颇颈颉颊颋颌颍颎颏颐频颒颓颔颕颖颗题颙颚颛颜额颞颟颠颡颢颣颤颥颦颧风飏飐飑飒飓飔飕飖飗飘飙飚飞飨餍饤饥饦饧饨饩饪饫饬饭饮饯饰饱饲饳饴饵饶饷饸饹饺饻饼饽饾饿馀馁馂馃馄馅馆馇馈馉馊馋馌馍馎馏馐馑馒馓馔馕马驭驮驯驰驱驲驳驴驵驶驷驸驹驺驻驼驽驾驿骀骁骂骃骄骅骆骇骈骉骊骋验骍骎骏骐骑骒骓骔骕骖骗骘骙骚骛骜骝骞骟骠骡骢骣骤骥骦骧髅髋髌鬓魇魉鱼鱽鱾鱿鲀鲁鲂鲄鲅鲆鲇鲈鲉鲊鲋鲌鲍鲎鲏鲐鲑鲒鲓鲔鲕鲖鲗鲘鲙鲚鲛鲜鲝鲞鲟鲠鲡鲢鲣鲤鲥鲦鲧鲨鲩鲪鲫鲬鲭鲮鲯鲰鲱鲲鲳鲴鲵鲶鲷鲸鲹鲺鲻鲼鲽鲾鲿鳀鳁鳂鳃鳄鳅鳆鳇鳈鳉鳊鳋鳌鳍鳎鳏鳐鳑鳒鳓鳔鳕鳖鳗鳘鳙鳛鳜鳝鳞鳟鳠鳡鳢鳣鸟鸠鸡鸢鸣鸤鸥鸦鸧鸨鸩鸪鸫鸬鸭鸮鸯鸰鸱鸲鸳鸴鸵鸶鸷鸸鸹鸺鸻鸼鸽鸾鸿鹀鹁鹂鹃鹄鹅鹆鹇鹈鹉鹊鹋鹌鹍鹎鹏鹐鹑鹒鹓鹔鹕鹖鹗鹘鹚鹛鹜鹝鹞鹟鹠鹡鹢鹣鹤鹥鹦鹧鹨鹩鹪鹫鹬鹭鹯鹰鹱鹲鹳鹴鹾麦麸黄黉黡黩黪黾鼋鼌鼍鼗鼹齄齐齑齿龀龁龂龃龄龅龆龇龈龉龊龋龌龙龚龛龟咨尝“”"
)


def fix_chinese_text_generation_space(text):
    output_text = text
    output_text = re.sub(
        r'([\u3401-\u9FFF+——！，。？、~@#￥%…&*（）：；《）《》“”()»〔〕\-!$^*()_+|~=`{}\[\]:";\'<>?,.·\/\\])\s([^0-9a-zA-Z])',
        r"\1\2",
        output_text,
    )
    output_text = re.sub(
        r'([^0-9a-zA-Z])\s([\u3401-\u9FFF+——！，。？、~@#￥%…&*（）：；《）《》“”()»〔〕\-!$^*()_+|~=`{}\[\]:";\'<>?,.·\/\\])',
        r"\1\2",
        output_text,
    )
    output_text = re.sub(
        r'([\u3401-\u9FFF+——！，。？、~@#￥%…&*（）：；《）《》“”()»〔〕\-!$^*()_+|~=`{}\[\]:";\'<>?,.·\/\\])\s([a-zA-Z0-9])',
        r"\1\2",
        output_text,
    )
    output_text = re.sub(
        r'([a-zA-Z0-9])\s([\u3401-\u9FFF+——！，。？、~@#￥%…&*（）：；《）《》“”()»〔〕\-!$^*()_+|~=`{}\[\]:";\'<>?,.·\/\\])',
        r"\1\2",
        output_text,
    )
    output_text = re.sub(r"＄\s([0-9])", r"＄\1", output_text)
    output_text = re.sub(",", "，", output_text)
    output_text = re.sub(
        r"([0-9])，([0-9])", r"\1,\2", output_text
    )  # fix comma in numbers
    # fix multiple commas
    output_text = re.sub(r"\s?[，]+\s?", "，", output_text)
    output_text = re.sub(r"\s?[、]+\s?", "、", output_text)
    # fix period
    output_text = re.sub(r"\s?[。]+\s?", "。", output_text)
    # fix ...
    output_text = re.sub(r"\s?\.{3,}\s?", "...", output_text)
    # fix exclamation mark
    output_text = re.sub(r"\s?[!！]+\s?", "！", output_text)
    # fix question mark
    output_text = re.sub(r"\s?[?？]+\s?", "？", output_text)
    # fix colon
    output_text = re.sub(r"\s?[:：]+\s?", "：", output_text)
    # fix quotation mark
    output_text = re.sub(r'\s?(["“”\']+)\s?', r"\1", output_text)
    # fix semicolon
    output_text = re.sub(r"\s?[;；]+\s?", "；", output_text)
    # fix dots
    output_text = re.sub(r"\s?([~●．…]+)\s?", r"\1", output_text)
    output_text = re.sub(r"\s?\[…\]\s?", "", output_text)
    output_text = re.sub(r"\s?\[\.\.\.\]\s?", "", output_text)
    output_text = re.sub(r"\s?\.{3,}\s?", "...", output_text)
    # fix slash
    output_text = re.sub(r"\s?[／/]+\s?", "／", output_text)
    # fix dollar sign
    output_text = re.sub(r"\s?[$＄]+\s?", "＄", output_text)
    # fix @
    output_text = re.sub(r"\s?([@＠]+)\s?", "＠", output_text)
    # fix baskets
    output_text = re.sub(
        r"\s?([\[\(<〖【「『（）』」】〗>\)\]]+)\s?", r"\1", output_text)

    return output_text


class TranslationPipeline(HfTranslationPipeline):
    def __init__(
        self,
        model,
        tokenizer,
        device=None,
        max_length=512,
        src_lang=None,
        tgt_lang=None,
        num_beams=3,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=1.0,
        repetition_penalty=1.0,
        length_penalty=1.0,
        sequence_bias=None,
        bad_words_ids=None,
        no_repeat_ngram_size=0,
    ):
        self.model = model
        self.tokenizer = tokenizer

        def get_tokens(word):
            return tokenizer([word], add_special_tokens=False).input_ids[0]

        bad_words_ids = [get_tokens(char) for char in hans_chars]

        super().__init__(
            self.model,
            self.tokenizer,
            device=device,
            max_length=max_length,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            num_beams=num_beams,
            do_sample=do_sample,
            top_k=top_k if do_sample == True else None,
            top_p=top_p if do_sample == True else None,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            length_penalty=length_penalty,
            sequence_bias=sequence_bias,
            bad_words_ids=bad_words_ids,
            no_repeat_ngram_size=no_repeat_ngram_size,
        )

    def postprocess(
        self,
        model_outputs,
        return_type=ReturnType.TEXT,
        clean_up_tokenization_spaces=True,
    ):
        records = super().postprocess(
            model_outputs,
            return_type=return_type,
            clean_up_tokenization_spaces=clean_up_tokenization_spaces,
        )
        for rec in records:
            translation_text = fix_chinese_text_generation_space(
                rec["translation_text"].strip()
            )

            rec["translation_text"] = translation_text
        return records

    def __call__(self, *args, **kwargs):
        records = super().__call__(*args, **kwargs)

        return records


if __name__ == "__main__":
    from transformers import BertTokenizerFast
    from optimum.onnxruntime import ORTModelForSeq2SeqLM

    model_id = "hon9kon9ize/bart-translation-zh-yue-onnx"

    tokenizer = BertTokenizerFast.from_pretrained(model_id)
    model = ORTModelForSeq2SeqLM.from_pretrained(model_id, use_cache=False)
    pipe = TranslationPipeline(model=model, tokenizer=tokenizer)

    print(
        pipe(
            "近年成为许多港人热门移居地的英国中部城巿诺定咸（又译诺丁汉，Nottingham），多年来一直面对财政困境，市议会周三（11月29日）宣布破产，是继英国第二大城市伯明翰今年9月宣布破产后，近期「爆煲」的另一个英国主要城市。诺定咸除了维持法例规定必须提供的服务外，巿政府将暂停所有非必要的公共开支。",
            max_length=300,
        )
    )
