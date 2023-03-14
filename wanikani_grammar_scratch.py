import requests, json, urllib, os, sys, math, time, random

## output directory
wanikani_dir = r'C:\tmp\WaniKani'

isExist = os.path.exists(wanikani_dir)
if not isExist:
    os.makedirs(wanikani_dir)
    print("Created new directory for your files")

verbs = ['intransitive verb', 'transitive verb']
verbtypes = ['godan','ichiban','suru']
adjectives = ['い adjective', 'な adjective']

address = 'https://api.wanikani.com/v2'
token = '8c6f5c7d-12ae-4201-a805-f791521ec135'
headers = {
    'object': 'vocabulary',
    'Authorization': f'Bearer {token}'
    }
endpoint = "subjects?types=vocabulary"
endpoint2 = "user"
headers2 = {
    'Authorization': f'Bearer {token}'
    }
print("\nHello! Welcome to the Wanikani Grammar Part-of-Speech Doodad.\n" +
      "Please wait while current data is gathered from the Wanikani server.\n")
current_level = 0

levelapicall = requests.get(f'{address}/{endpoint2}', headers=headers)
levelapicall_json = levelapicall.json()
current_level = levelapicall_json['data']['level']

apicall = requests.get(f'{address}/{endpoint}', headers=headers)
apicall_json = apicall.json()
works_count = apicall_json['total_count']
page_count = math.ceil(works_count / 1000)

with open(wanikani_dir + "\\" + "apitest" + ".json", "w") as outfile:
    json.dump(apicall_json, outfile)

# print(apicall.request.url)
# print(apicall.request.body)
# print(apicall.request.headers)

vocablist = []
verblist = []
nounlist = []
adjectivelist = []

for i in range(0, page_count):
    data = apicall_json
    for i in data['data']:
        vocabentry = {}
        vocabentry['character'] = i['data']['characters']
        vocabentry['meaning'] = i['data']['meanings'][0]['meaning']
        vocabentry['kanji'] = i['data']['characters']
        vocabentry['part_of_speech_1'] = None
        vocabentry['part_of_speech_2'] = None
        vocabpart = i['data']['parts_of_speech']
        vocablevel = i['data']['level']
        if len(vocabpart) == 2:
            vocabentry['part_of_speech_1'] = vocabpart[0]
            vocabentry['part_of_speech_2'] = vocabpart[1]
        elif len(vocabpart) == 1:
            vocabentry['part_of_speech_1'] = vocabpart[0]
        if vocablevel <= current_level:
            vocablist.append(vocabentry)
    # for i in vocablist:
    #     print(str(i) + '\n')
    apicallpage = apicall_json['pages']['next_url']
    if apicallpage == None:
        break
    newapicall = requests.get(apicallpage, headers=headers)
    newapicall_json = newapicall.json()
    apicall = newapicall
    apicall_json = newapicall_json
    print(".   .   .   .   .\n")
with open(wanikani_dir + "\\" + "vocabdata" + '.txt', 'w', encoding="utf-8") as vocabdata:
    for i in vocablist:
        vocabdata.writelines(str(i) + '\n\n')

verbcount = 0
adjectivecount = 0

for i in vocablist:
    character = i['character']
    meaning = i['meaning']
    type_of_word = i['part_of_speech_1']
    if type_of_word in verbs:
        verbcount += 1
        i['id'] = verbcount
        if i['part_of_speech_2'] == 'godan verb':
            i['part_of_speech_2'] = 'godan'
        elif i['part_of_speech_2'] == 'ichidan verb':
            i['part_of_speech_2'] = 'ichidan'
        elif i['part_of_speech_2'] == 'する verb' or i['part_of_speech_2'] == 'する verb':
            i['part_of_speech_2'] = 'suru'
        verblist.append(i)

    elif type_of_word in adjectives:
        adjectivecount += 1
        i['id'] = adjectivecount
        adjectivelist.append(i)

    elif type_of_word == 'noun':
        nounlist.append(i)

    # if character == kanji_input:
    #     print(meaning)

# print(len(verblist))
# print(len(adjectivelist))
# print(len(nounlist))

print("\nThis tool builds upon the Wanikani kanji learning system\n" +
      "to provide extra study of the various kinds of verbs and\n" +
      "adjectives that you've learned up to now.\n")

print("Your current Wanikani level is " + str(current_level) + ";\n" +
    "you'll only be tested on vocabulary that you know.\n")

while True:
    affirmativelist = ['Y', 'y', 'yes', 'Yes']
    negativelist = ['N', 'n', 'no', 'No']
    verbresponses = ['verbs', 'verb']
    adjectiveresponses = {'na': "な adjective", 'i':'い adjective'}
    studylist = []
    partpicker = input("\nWould you like to study verbs or adjectives?:_")
    if partpicker in verbresponses:
        partselection = 'verbs'
        while partselection == 'verbs':
            studylist = verblist
            selected_item = random.choice(verblist)
            print("\n" + selected_item['kanji'])
            verb_type = selected_item['part_of_speech_2']
            answer = input("\nIs this a godan, ichidan, or suru verb?:_")
            if answer == verb_type:
                time.sleep(.5)
                print('\nCorrect! Meaning: ' + ' \"'+ str(selected_item['meaning']) + '\". ')
                time.sleep(.5)
                wanttocontinue = input('\n\nNext question?:_')
                if wanttocontinue in affirmativelist:
                    continue
                else:
                    partselction = 'ver'
                    break
            else:
                time.sleep(.5)
                print('\nWrong! Here is the right answer: ' + str(verb_type) + ". Meaning:" + ' \"'+ str(selected_item['meaning']) + '.\"')
                time.sleep(.5)
                wanttocontinue = input('\n\nNext question?:_')
                if wanttocontinue in affirmativelist:
                    continue
                else:
                    partselection = ''
                    studylist = []
                    break

    elif partpicker == "adjectives":
        partselection = 'adjectives'
        while partselection == 'adjectives':
            studylist = adjectivelist
            selected_item = random.choice(adjectivelist)
            print("\n" + selected_item['kanji'])
            adjective_type = selected_item['part_of_speech_1']
            answer = input("\nIs this an い-adjective or a な-adjective?:_")
            answer_input = adjectiveresponses[answer]
            if answer_input == adjective_type:
                time.sleep(.5)
                print('\nCorrect! Meaning: ' + ' \"' + str(selected_item['meaning']) + '\". ')
                time.sleep(.5)
                wanttocontinue = input('\n\nNext question?:_')
                if wanttocontinue in affirmativelist:
                    continue
                else:
                    partselction = 'ver'
                    break
            else:
                time.sleep(.5)
                print('\nWrong! Here is the right answer: ' + str(adjective_type) + ". Meaning:" + ' \"' + str(
                    selected_item['meaning']) + '.\"')
                time.sleep(.5)
                wanttocontinue = input('\n\nNext question?:_')
                if wanttocontinue in affirmativelist:
                    continue
                else:
                    partselection = ''
                    studylist = []
                    break
    else:
        break