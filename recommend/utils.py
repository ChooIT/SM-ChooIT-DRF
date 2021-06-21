import re
import datetime
import os


# Image File Upload Utilities
def set_filename_format(now, instance, filename):
    return "{username}-{date}-{microsecond}{extension}" \
        .format(username=instance.user_no,
                date=str(now.date()),
                microsecond=now.microsecond,
                extension=os.path.splitext(filename)[1])


def user_directory_path(instance, filename):
    now = datetime.datetime.now()
    path = "images/{year}/{month}/{day}/{username}/{filename}" \
        .format(year=now.year,
                month=now.month,
                day=now.day,
                username=instance.user_no,
                filename=set_filename_format(now, instance, filename))
    return path


# Review Text Utilities
def is_img_tag(html_text):
    index = html_text.index('<p>')
    if html_text[index + 3:index + 8] == '<img ':
        return True
    return False


def get_first_p_tag_value(html_text: str):
    open_p_index_list = [i.start() for i in re.finditer('<p>', html_text)]
    close_p_index_list = [i.start() for i in re.finditer('</p>', html_text)]
    for index in range(0, len(open_p_index_list)):
        if is_img_tag(html_text[open_p_index_list[index]:close_p_index_list[index]]):
            continue
        else:
            return html_text[open_p_index_list[index] + 3:close_p_index_list[index]]

