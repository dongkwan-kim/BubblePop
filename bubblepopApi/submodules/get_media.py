import json
from apiapp.models import Media

if __name__ == "__main__":
    json_data=open("./submodules/news_media.json").read()

    data = json.loads(json_data)
    print(data)



def save_media():
    json_data=open("./submodules/news_media.json").read()

    data = json.loads(json_data)
    media = Media.objects.all()
    for medium in data:

        exist_medium = media.filter(name = medium['name'])
        if exist_medium.exists():
            exist_medium = exist_medium[0]
            exist_medium.rss_list=medium['rss']
            exist_medium.political_view=medium['affinity']
            exist_medium.icon=medium['icon']
            exist_medium.mid=medium['mid']
            exist_medium.save()
        else:
            print(medium['name'])
            media.create(
                name=medium['name'],
                rss_list=medium['rss'],
                political_view=medium['affinity'],
                icon=medium['icon'],
                mid=medium['mid'],
                )
    return

