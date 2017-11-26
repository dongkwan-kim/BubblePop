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
    media.delete()
    for medium in data:
        media.create(
            name=medium['name'],
            rss_list=medium['rss'],
            political_view=medium['affinity'],
            icon=medium['icon'],
            )


