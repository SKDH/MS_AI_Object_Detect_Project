"""
    json으로 되있는 라벨 데이터를 중 이미지 속 동물과 다른 동물로 작성되있는 annotaions 수정
    
    파일이 있는 동물 폴더를 기준으로 수정함
"""
import glob
import json
from tqdm import tqdm

ANIMALS = ["고라니", "멧돼지", "반달가슴곰"]
FOLDERS = {"반달가슴곰": "asian_black_bear", "고라니": "water_dear", "멧돼지": "wild_boar"}


# annation이 잘 못 작성된 파일 목록 가져오기
def get_json_values(directory, outer_key, inner_key):
    species_list = []
    multi_detect = 0
    solo_detect = 0
    animal_dict = {"multi_animal": []}
    filter_dict = {"반달가슴곰": [], "고라니": [], "멧돼지": []}
    for filepath in tqdm(glob.glob(directory + "/**/*.json", recursive=True)):
        with open(filepath, "r", encoding="utf8") as f:
            filename = filepath.split("\\")[-1].replace(".json", "")
            data = json.load(f)
            species_set = set()
            for item in data[outer_key]:
                species_set.add(item[inner_key])
                if item[inner_key] in ANIMALS:
                    if "asian_black_bear" in filepath and item[inner_key] != "반달가슴곰":
                        filter_dict["반달가슴곰"].append(filepath)
                    elif "water_dear" in filepath and item[inner_key] != "고라니":
                        filter_dict["고라니"].append(filepath)
                    elif "wild_boar" in filepath and item[inner_key] != "멧돼지":
                        filter_dict["멧돼지"].append(filepath)
            species_list.extend(species_set)
            if len(species_set) > 1:
                multi_detect += 1
                animal_dict["multi_animal"].append(filename)
            else:
                solo_detect += 1
                for animal in species_set:
                    if animal not in animal_dict:
                        animal_dict[animal] = []
                    animal_dict[animal].append(filename)
    return species_list, multi_detect, solo_detect, animal_dict, filter_dict


directory = "./wild_animals"  # 디렉토리 경로
outer_key = "annotations"  # 외부 키
inner_key = "species"  # 내부 키
species_list, multi_detect, solo_detect, animal_dict, filter_dict = get_json_values(
    directory, outer_key, inner_key
)
values_set = set(species_list)
print(values_set)
for i in values_set:
    print(f"{i}: {species_list.count(i)}")
print(f"다중 동물: {multi_detect}")
print(f"단일 동물: {solo_detect}")
print(animal_dict.keys())

if sum(len(v) for v in filter_dict.values()) > 0:
    print(f"수정 필요 파일: {len(filter_dict)}개")
    for animal in tqdm(filter_dict):
        for filepath in filter_dict[animal]:
            folder = filepath.split("\\")[-2]
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

                # 반달가슴곰 annotaion
                asian_black_bear_anno = {
                    "category_id": 6,
                    "category_name": "thibetanus",
                    "nocturnality": "yes",
                    "hazardous": "no",
                    "temperature": None,
                    "regularity": None,
                    "color": "검은색",
                    "shape": "초승달 모양 가슴 흰색털, 짧은 꼬리, 짧고 뾰족한 코, 넓적한 이마, 돌출형 귀.",
                    "size": "130~190cm",
                    "class": "포유동물강",
                    "order": "식육목",
                    "family": "곰과",
                    "genus": "곰속",
                    "species": "반달가슴곰",
                }

                # 고라니 annotaions
                water_dear_anno = {
                    "category_id": 1,
                    "category_name": "inermis",
                    "nocturnality": "yes",
                    "hazardous": "yes",
                    "temperature": None,
                    "regularity": None,
                    "color": "담갈적색",
                    "shape": "둥근귀, 뿔 없음, 엄니모양 송곳니, 짧은 꼬리.",
                    "size": "75~100cm",
                    "class": "포유동물강",
                    "order": "우제목",
                    "family": "사슴과",
                    "genus": "고라니속",
                    "species": "고라니",
                }

                # 멧돼지 annotaions
                wild_boar_anno = {
                    "category_id": 2,
                    "category_name": "scrofa",
                    "nocturnality": "yes",
                    "hazardous": "yes",
                    "temperature": None,
                    "regularity": None,
                    "color": "갈색 또는 검은색",
                    "shape": "원뿔형 머리, 삼각형 귀, 긴 주둥이, 짧고 가는 다리, 짧은 꼬리, 예리한 엄니.",
                    "size": "90~200cm",
                    "class": "포유동물강",
                    "order": "우제목",
                    "family": "멧돼지과",
                    "genus": "멧돼지속",
                    "species": "멧돼지",
                }

                # annotations를 순회하며 species 확인
                for annotation in data["annotations"]:
                    # 고라니, 멧돼지, 반달가슴곰만 확인
                    if annotation["species"] in ANIMALS:
                        if folder == "water_dear":
                            # 각 항목을 새로운 값으로 변경
                            for key, new_value in water_dear_anno.items():
                                annotation[key] = new_value
                        if folder == "wild_boar":
                            for key, new_value in wild_boar_anno.items():
                                annotation[key] = new_value
                        if folder == "asian_black_bear":
                            for key, new_value in asian_black_bear_anno.items():
                                annotation[key] = new_value

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    print("수정 끝")
else:
    print("수정 필요 파일 없음")
