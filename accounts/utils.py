from random import choice
from accounts.models import Nickname, NicknameArchive


def get_nickname():
    nickname = ""
    count = 1

    adj_list = Nickname.objects.filter(part='a').values_list('content')
    adj = choice(adj_list)[0]
    noun_list = Nickname.objects.filter(part='n').values_list('content', 'emoji')
    noun = choice(noun_list)
    emoji = noun[1]

    nickname = adj + noun[0]

    try:
        archive = NicknameArchive.objects.get(nickname=nickname)
        count = archive.count
        archive.count += 1
        archive.save()
    except NicknameArchive.DoesNotExist:
        NicknameArchive.objects.create(nickname=nickname)

    return emoji, nickname+str(count)
