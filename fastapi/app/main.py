import os

import pymongo

from fastapi import FastAPI

app = FastAPI()

USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password")

mongo = pymongo.MongoClient(f"mongodb://{USER}:{PASSWORD}@mongo:27017/")
collection = mongo.persona.keywords


@app.get("/persona")
def get_persona():
    return {doc["name"]: doc["keywords"] for doc in collection.find()}


@app.get("/persona/random")
def get_random_persona():
    random = collection.aggregate([{"$sample": {"size": 1}}]).next()
    random.pop("_id")
    return random


@app.get("/persona/{name}")
def get_persona_detail(name: str):
    doc = collection.find_one({"name": name})
    if doc:
        doc.pop("_id")
        return doc
    return {"ok": False, "msg": f"persona {name} not exist"}


@app.post("/persona")
def create_persona(name: str, topic: str, target: str, keywords: str):
    if collection.find_one({"name": name}):
        return {"ok": False, "msg": f"persona {name} already exist"}
    collection.insert_one(
        {"name": name, "topic": topic, "target": target, "keywords": keywords}
    )
    return {"ok": True, "msg": "persona {name} created"}


@app.delete("/persona")
def delete_persona(name: str):
    if collection.find_one_and_delete({"name": name}):
        return {"ok": True, "msg": "persona {name} deleted"}
    return {"ok": False, "msg": f"persona {name} not exist"}


@app.post("/reset")
def reset_database():
    init_persona = [
        {
            "name": "스마트팩토리",
            "topic": "4차산업,스마트팩토리,IoT,AI,빅데이터",
            "target": "기업인,4차산업열정가",
            "keywords": "스마트팩토리,사물인터넷,인공지능,빅데이터",
        },
        {
            "name": "런치타임",
            "topic": "간편도시락레시피",
            "target": "주부,직장인",
            "keywords": "점심메뉴,데일리밀박스,반찬,도시락",
        },
        {
            "name": "슈슈요리조리",
            "topic": "간단요리레시피",
            "target": "초보주부",
            "keywords": "간편요리,가정식,한끼요리,쉬운레시피,홈쿡",
        },
        {
            "name": "좋은생각",
            "topic": "긍정마인드",
            "target": "실천자",
            "keywords": "긍정성,자기계발,행복,치유,성장",
        },
        {
            "name": "테크놀로지스트",
            "topic": "기술제품리뷰",
            "target": "IT제품구매자",
            "keywords": "전자제품,제품리뷰,스마트홈,기술트렌드,로봇,메타버스",
        },
        {
            "name": "테크마스터",
            "topic": "기술과전자제품",
            "target": "기술열정가",
            "keywords": "최신기술,반도체,하드웨어,센서",
        },
        {
            "name": "두뇌활성화",
            "topic": "기억력향상법",
            "target": "뇌활동애호가",
            "keywords": "기억법,집중력강화,인지능력,퀴즈,퍼즐",
        },
        {
            "name": "나폴리맘",
            "topic": "다문화가족이야기",
            "target": "다문화가족생활",
            "keywords": "이민,언어교육,문화차이극복,정체성",
        },
        {
            "name": "스텝별댄스",
            "topic": "댄스튜토리얼",
            "target": "댄스애호가",
            "keywords": "댄스,춤,안무,발레,스트레칭",
        },
        {
            "name": "한솥도시락",
            "topic": "도시락레시피",
            "target": "직장인,주부",
            "keywords": "도시락,점심메뉴,한끼요리,반찬,데일리밀박스",
        },
        {
            "name": "책과문학애호가",
            "topic": "독서와문학",
            "target": "독서애호가",
            "keywords": "베스트셀러,문학작품,독서,북리뷰,작가인터뷰",
        },
        {
            "name": "솔로탱이의일기",
            "topic": "독신자일상",
            "target": "독신여성",
            "keywords": "독신,1인가구,배낭여행,혼밥",
        },
        {
            "name": "마블링세상",
            "topic": "마블링아트",
            "target": "마블링애호가",
            "keywords": "공예,레진아트,폴리머클레이,입체프린팅",
        },
        {
            "name": "마인드풀생각",
            "topic": "마인드풀니스",
            "target": "마인드풀니스실천자",
            "keywords": "마인드풀니스,명상,자기성찰,힐링",
        },
        {
            "name": "맛팡팡",
            "topic": "먹방",
            "target": "먹방애호가",
            "keywords": "먹방,음식리뷰,코리아푸드,직접만든음식",
        },
        {
            "name": "뷰티블리썸",
            "topic": "메이크업과뷰티",
            "target": "뷰티관심자",
            "keywords": "메이크업튜토리얼,뷰티제품리뷰,성형정보,헤어스타일",
        },
        {
            "name": "띵작대디",
            "topic": "목공예와집수리",
            "target": "주말목수",
            "keywords": "목공예,집수리,공구리뷰,인테리어아이디어",
        },
        {
            "name": "예술과창작",
            "topic": "미술과창작",
            "target": "예술애호가",
            "keywords": "미술작품,조각,창작프로세스,전시회,아트마켓",
        },
        {
            "name": "펫츠둥이",
            "topic": "반려동물관리",
            "target": "반려동물주인",
            "keywords": "강아지놀이,강아지훈련,펫샵,동물병원",
        },
        {
            "name": "고양이애호가",
            "topic": "반려동물과고양이",
            "target": "고양이열정가",
            "keywords": "고양이종류,돌봄팁,반려동물용품,고양이산책",
        },
        {
            "name": "오감댄스",
            "topic": "발레수업",
            "target": "발레애호가",
            "keywords": "발레,무용,스트레칭,에어로빅,댄스스포츠",
        },
        {
            "name": "꿀꿀홈베이킹",
            "topic": "베이킹레시피",
            "target": "베이커",
            "keywords": "베이킹,디저트,케이크,마카롱,쿠키",
        },
        {
            "name": "비건화장꾼",
            "topic": "비건뷰티",
            "target": "비건",
            "keywords": "비건화장품,동물권,동물실험반대,동물보호",
        },
        {
            "name": "빈티지디제인",
            "topic": "빈티지DIY인테리어",
            "target": "인테리어애호가",
            "keywords": "빈티지인테리어,업사이클,핸드메이드",
        },
        {
            "name": "스냅해커",
            "topic": "해킹및보안",
            "target": "해커,IT보안전문가",
            "keywords": "해킹,사이버보안,디지털포렌식,보안리뷰,암호화폐",
        },
        {
            "name": "스포츠연애가",
            "topic": "스포츠와경기관람",
            "target": "스포츠팬",
            "keywords": "스포츠팀,경기일정,스포츠뉴스,응원가,선수인터뷰",
        },
        {
            "name": "플랜티타임",
            "topic": "식물키우기",
            "target": "식물애호가",
            "keywords": "실내정원,텃밭가꾸기,꽃꽂이,원예,정원가꾸기",
        },
        {
            "name": "꿈꾸는아이",
            "topic": "아동교육",
            "target": "학부모",
            "keywords": "유아교육,창의력교육,놀이활동,아동동화,유아영어",
        },
        {
            "name": "밥아빠",
            "topic": "아빠육아",
            "target": "아빠",
            "keywords": "아빠육아,부성경험기,가족활동,엄마돕기",
        },
        {
            "name": "모험왕마누",
            "topic": "야외활동과모험",
            "target": "모험애호가",
            "keywords": "등산,캠핑,생태관찰,환경보호,야생,국립공원탐방",
        },
        {
            "name": "엔터테인먼트중독",
            "topic": "엔터테인먼트소식",
            "target": "엔터테인먼트팬",
            "keywords": "영화,드라마,콘서트,스타소식,공연리뷰,인터뷰",
        },
        {
            "name": "여행열정가",
            "topic": "여행과모험",
            "target": "여행객",
            "keywords": "해외여행,외국어,어드벤처,가족여행",
        },
        {
            "name": "영어킹",
            "topic": "영어교육",
            "target": "영어학습자",
            "keywords": "영어공부,회화,발음교정,해외유학,시험대비",
        },
        {
            "name": "영화비평가",
            "topic": "영화평론및리뷰",
            "target": "영화애호가",
            "keywords": "영화리뷰,영화평론,개봉작분석,영화이론,관객반응",
        },
        {
            "name": "굿모닝요가",
            "topic": "요가와명상",
            "target": "요가애호가",
            "keywords": "요가,명상,스트레칭,호흡요법,비욘드요가,필라테스",
        },
        {
            "name": "맘스쿠킹클래스",
            "topic": "요리교실",
            "target": "주부",
            "keywords": "요리교실,밀키트,홈쿠킹,베이킹클래스,아이밥만들기",
        },
        {
            "name": "와이너",
            "topic": "와인과안주",
            "target": "와인애호가",
            "keywords": "안주,와인바,쉐프인터뷰,와인페어링",
        },
        {
            "name": "요리마스터",
            "topic": "요리및레시피",
            "target": "요리열정가",
            "keywords": "푸드스타일링,쿠킹클래스,레스토랑리뷰,도구소개",
        },
        {
            "name": "피트니스프로",
            "topic": "운동및피트니스",
            "target": "피트니스열정가",
            "keywords": "운동루틴,식단,피트니스,헬스장",
        },
        {
            "name": "또똣동",
            "topic": "유아교육과놀이",
            "target": "학부모,유아교육자",
            "keywords": "유아교육,놀이활동,창의력교육,동화읽기,상상놀이",
        },
        {
            "name": "귀여운똘이",
            "topic": "육아일상",
            "target": "엄마",
            "keywords": "육아일상,양육정보,모유수유,이유식,유아발달",
        },
        {
            "name": "음악매니아",
            "topic": "음악과음악가",
            "target": "음악애호가",
            "keywords": "음악장르,음악가인터뷰,공연정보,악기연주법,뮤직비디오",
        },
        {
            "name": "일렉트로닉",
            "topic": "일렉트로닉음악",
            "target": "일렉트로닉음악애호가",
            "keywords": "일렉트로닉,클럽음악,댄스음악,뮤직페스티벌,디제잉",
        },
        {
            "name": "브이로거",
            "topic": "일상브이로그",
            "target": "일상기록애호가",
            "keywords": "브이로그,일상,일기,기록,챌린지",
        },
        {
            "name": "조커쵸크",
            "topic": "일상코미디스케치",
            "target": "코미디애호가",
            "keywords": "일상유머,코미디스케치,개그콘텐츠,예능,팟캐스트",
        },
        {
            "name": "오늘도잘살아보자",
            "topic": "자기계발",
            "target": "자기계발애호가",
            "keywords": "인생교훈,자기계발서적,행복연구,리딩클럽,행복수업",
        },
        {
            "name": "자동차매니아",
            "topic": "자동차와모터스포츠",
            "target": "자동차열정가",
            "keywords": "자동차브랜드,레이싱,자동차튜닝,오토바이,경주분석",
        },
        {
            "name": "자연탐험가",
            "topic": "자연탐험및야외활동",
            "target": "모험가",
            "keywords": "등산,생태관찰,환경보호,사파리,국립공원탐방",
        },
        {
            "name": "똑똑하게투자",
            "topic": "주식투자정보",
            "target": "투자자",
            "keywords": "주식,재테크,주식분석,부동산,가상자산,자산관리",
        },
        {
            "name": "골목길킹",
            "topic": "지역맛집탐방",
            "target": "맛집탐방가",
            "keywords": "맛집탐방,로컬푸드,동네가게,숨은맛집,먹거리추천",
        },
        {
            "name": "차돌바위가이드",
            "topic": "지역여행정보",
            "target": "여행객",
            "keywords": "로컬여행,지역명소,맛집,로컬투어,숨은여행코스",
        },
        {
            "name": "아트인하우스",
            "topic": "집꾸미기아이디어",
            "target": "인테리어애호가",
            "keywords": "인테리어,집꾸미기,가구배치,소품추천,리폼",
        },
        {
            "name": "청춘불편한진실",
            "topic": "청년실업문제",
            "target": "청년",
            "keywords": "청년실업,일자리,주거문제,구직팁,해외취업",
        },
        {
            "name": "고백왕",
            "topic": "청춘로맨스",
            "target": "10대",
            "keywords": "연애,고백,문화,데이트코스,선물아이디어",
        },
        {
            "name": "모닝커피",
            "topic": "커피리뷰와레시피",
            "target": "커피애호가",
            "keywords": "커피,카페투어,원두추천,커피맛집",
        },
        {
            "name": "클래식맘",
            "topic": "클래식음악",
            "target": "클래식애호가",
            "keywords": "클래식,오페라,연주회,악기연주법,음악이론",
        },
        {
            "name": "재테크대학",
            "topic": "투자정보",
            "target": "투자자",
            "keywords": "주식,부동산,정보금융,비트코인,스타트업투자",
        },
        {
            "name": "미스터리더",
            "topic": "팟캐스트소개",
            "target": "팟캐스트리스너",
            "keywords": "팟캐스트,오디오북,스토리텔링,크리에이터인터뷰,제작노하우",
        },
        {
            "name": "패션스타일러",
            "topic": "패션과스타일",
            "target": "패션열정가",
            "keywords": "패션트렌드,의류브랜드,스타일링,메이크업,빈티지패션",
        },
        {
            "name": "곤충샵",
            "topic": "곤충정보",
            "target": "곤충애호가",
            "keywords": "곤충소개,해충,희귀곤충,모기,퇴치법",
        },
        {
            "name": "포토샵신학생",
            "topic": "포토샵튜토리얼",
            "target": "포토샵초보자",
            "keywords": "포토샵,그래픽디자인,포스터,포토샵팁",
        },
        {
            "name": "자연속의그림자",
            "topic": "풍경사진",
            "target": "풍경사진작가",
            "keywords": "풍경사진,야경,여행,사진구도,카메라리뷰",
        },
        {
            "name": "달려라김치만두",
            "topic": "한식레시피",
            "target": "한식애호가",
            "keywords": "한식,김치,젓갈,한식요리법,계절음식",
        },
        {
            "name": "환경지킴이",
            "topic": "환경보호및지속가능성",
            "target": "환경활동가",
            "keywords": "재활용,친환경생활,지속가능에너지,기후행동,미세먼지",
        },
        {
            "name": "수면과학",
            "topic": "ASMR수면유도",
            "target": "수면문제해결자",
            "keywords": "백색소음,수면유도,호흡법,수면음악",
        },
        {
            "name": "K-POP팬",
            "topic": "K-POP뉴스",
            "target": "K-POP팬",
            "keywords": "케이팝,아티스트분석,아이돌,팬커뮤니티,댄스",
        },
        {
            "name": "드라마리뷰어",
            "topic": "드라마리뷰",
            "target": "드라마시청자",
            "keywords": "드라마리뷰,배우인터뷰,에피소드해설,요약본,몰아보기",
        },
        {
            "name": "예능프로그램애호가",
            "topic": "예능프로그램리뷰",
            "target": "예능프로그램시청자",
            "keywords": "예능,하이라이트,베스트클립,리액션,예능레전드",
        },
        {
            "name": "강아지훈련전문가",
            "topic": "강아지훈련방법",
            "target": "강아지훈련에도움이필요한사람들",
            "keywords": "강아지훈련,행동교정,반려견,애완동물관리,애견훈련사",
        },
        {
            "name": "히스토리텔러",
            "topic": "역사이야기및강의",
            "target": "역사에관심있는사람들",
            "keywords": "역사,한국사,히스토리,역사강의,역사이야기",
        },
        {
            "name": "심리카운셀러",
            "topic": "심리학강의및심리상담",
            "target": "심리학에관심있는사람들",
            "keywords": "심리학,상담,심리치료사,심리테스트,검사",
        },
        {
            "name": "리걸어드바이저",
            "topic": "법률상담및법률정보제공",
            "target": "법률상담이필요한사람들",
            "keywords": "법률,상담,법률정보,변호사,소송,법률자문",
        },
        {
            "name": "경제교육가",
            "topic": "경제원리설명,경제이론",
            "target": "경제에대해배우고싶은사람",
            "keywords": "경제원리,이론,경제사,경제교육,경제학자",
        },
        {
            "name": "조경디자이너",
            "topic": "조경디자인아이디어및팁",
            "target": "조경디자인에관심있는사람들",
            "keywords": "조경,디자인,정원,조경아이디어,조경디자인팁",
        },
        {
            "name": "프로축구해설가",
            "topic": "축구경기분석,리그뉴스",
            "target": "축구에대한전문적인분석과뉴스를찾는사람들",
            "keywords": "경기분석,축구,축구해설,하이라이트,해외축구",
        },
        {
            "name": "야구엔터테이너",
            "topic": "야구경기하이라이트,선수인터뷰,놀이기록",
            "target": "야구에대한흥미로운콘텐츠를찾는사람들",
            "keywords": "야구하이라이트,선수인터뷰,사회인야구,야구직관,",
        },
        {
            "name": "빈티지패션컬렉터",
            "topic": "빈티지패션아이템",
            "target": "빈티지스타일을즐기는사람들",
            "keywords": "빈티지패션,스타일링팁,쇼핑가이드,빈티지아이템",
        },
        {
            "name": "패션DIY크리에이터",
            "topic": "패션재활용팁",
            "target": "독특하고개성있는스타일을추구하는사람들",
            "keywords": "패션,헌옷,리폼,패션재활용,옷만들기",
        },
        {
            "name": "코딩마스터",
            "topic": "코딩튜토리얼",
            "target": "코딩을배우고싶은사람들",
            "keywords": "코딩,프로그래밍,튜토리얼,개발팁,프로그래밍언어",
        },
        {
            "name": "스타트업핵심인물",
            "topic": "스타트업운영및비즈니스팁",
            "target": "스타트업에관심있는사람들",
            "keywords": "스타트업,비즈니스,창업,기업가치,투자",
        },
        {
            "name": "음악프로듀서",
            "topic": "음악제작과정",
            "target": "음악제작에관심이있는사람들",
            "keywords": "음악제작,프로듀싱팁,장비리뷰,음악프로듀서",
        },
        {
            "name": "인디음악애호가",
            "topic": "인디음악추천",
            "target": "인디음악리스너",
            "keywords": "인디음악,음악추천,아티스트인터뷰,음악리뷰",
        },
        {
            "name": "IT트렌드워처",
            "topic": "IT트렌드",
            "target": "IT업계의최신트렌드와뉴스에관심있는사람들",
            "keywords": "정보기술트렌드,기술뉴스,산업동향,최신기술",
        },
        {
            "name": "게임개발자",
            "topic": "게임개발",
            "target": "게임개발에관심있는사람들",
            "keywords": "게임개발,인디게임,게임디자인,개발자,프로그래밍",
        },
        {
            "name": "건축마스터",
            "topic": "건축디자인및아이디어",
            "target": "건축디자인에관심있는사람들",
            "keywords": "건축,디자인,건축가,건축디자인,건축물",
        },
        {
            "name": "백패커가이드",
            "topic": "저렴한여행",
            "target": "저렴하게여행하고싶은사람들",
            "keywords": "백패킹,저렴한여행,배낭여행,숙박추천,가성비",
        },
        {
            "name": "비건요리전문가",
            "topic": "비건레시피",
            "target": "비건또는식물기반식사를선호하는사람들",
            "keywords": "비건,샐러드,식재료,채식,요리팁",
        },
        {
            "name": "러닝열정가",
            "topic": "러닝루틴,러닝팁",
            "target": "달리기를즐기는사람들",
            "keywords": "러닝,조깅,러닝팁,러닝화,마라톤",
        },
        {
            "name": "보컬코치",
            "topic": "노래가이드및보컬트레이닝",
            "target": "노래에관심있는사람들",
            "keywords": "노래,가이드,보컬,트레이닝,레슨,보컬트레이너",
        },
        {
            "name": "스트리트패션리스타",
            "topic": "스트리트패션트렌드",
            "target": "독특하고대담한스타일을추구하는사람들",
            "keywords": "스트리트패션,트렌드,옷조합,패션리뷰,브랜드",
        },
        {
            "name": "캠핑마스터",
            "topic": "캠핑가이드및팁",
            "target": "캠핑에관심있는사람들",
            "keywords": "캠핑,아웃도어,캠핑가이드,캠핑팁,캠핑장비",
        },
        {
            "name": "판타지사이언티스트",
            "topic": "공상과학이야기및이론",
            "target": "공상과학에관심있는사람들",
            "keywords": "공상과학,이론,사이언스,이야기",
        },
        {
            "name": "테이블세팅아티스트",
            "topic": "테이블세팅아이디어",
            "target": "홈파티를즐기는사람들",
            "keywords": "테이블세팅,홈파티,디너파티,인테리어,세팅아이디어",
        },
        {
            "name": "드론마스터",
            "topic": "드론비디오촬영및편집",
            "target": "드론촬영에관심있는사람들",
            "keywords": "드론,비디오촬영,촬영팁,드론비디오,비디오편집",
        },
        {
            "name": "문화탐험가",
            "topic": "세계문화,역사적장소",
            "target": "다양한문화와역사에관심있는사람들",
            "keywords": "세계문화,역사적장소,예술작품,문화탐험,여행가이드",
        },
        {
            "name": "재즈열정가",
            "topic": "재즈음악감상,아티스트소개",
            "target": "재즈에대한이해를높이고싶은사람들",
            "keywords": "재즈음악,아티스트소개,재즈공연,음악감상",
        },
        {
            "name": "미니멀리스트",
            "topic": "미니멀라이프팁및경험공유",
            "target": "미니멀리즘에관심있는사람들",
            "keywords": "미니멀리즘,미니멀라이프,미니멀,일상,라이프스타일",
        },
        {
            "name": "수학마스터",
            "topic": "수학문제해설,수학공식",
            "target": "수학에어려움을겪고있는학생들",
            "keywords": "수학문제해설,수학공식,공부팁,수학학습",
        },
        {
            "name": "럭셔리트래블러",
            "topic": "고급호텔리뷰",
            "target": "고급여행을즐기고싶은사람들",
            "keywords": "럭셔리여행,고급호텔,호텔식당,브이로그",
        },
        {
            "name": "아스트로노머",
            "topic": "천체관측팁및정보",
            "target": "천문학에관심있는사람들",
            "keywords": "천체관측,별,우주,천문학",
        },
    ]
    if "persona" in mongo.list_database_names():
        mongo.drop_database("persona")
    collection.insert_many(init_persona)
    return {"ok": True, "msg": "persona reset done"}
