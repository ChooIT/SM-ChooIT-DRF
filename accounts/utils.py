from random import choice
from accounts.models import Nickname, NicknameArchive


def get_nickname():
    nickname = ""
    count = 0

    adj_list = Nickname.objects.values_list(part="a")
    adj = choice(adj_list)
    noun_list = Nickname.objects.values_list(part="n")
    noun = choice(noun_list)
    emoji = noun.emoji

    nickname = adj + noun

    try:
        archive = NicknameArchive.objects.get(nickname=nickname)
        count = archive.count
        archive.count += 1
        archive.save()
    except Nickname.DoesNotExist:
        Nickname.objects.create(nickname=nickname)

    return emoji, nickname+str(count)
