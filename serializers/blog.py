# in this file we serialize the data, a.k.a. decode it

def DecodeBlog(data) -> dict:
    return {
        "_id": str(data["_id"]),
        "title": data["title"],
        "sub_title": data["sub_title"],
        "content": data["content"],
        "author": data["author"],
        "date": data["date"],
        "tags": data["tags"]
                }

# do it for multiple blogs
def DecodeBlogs(datas) -> list:
    return [DecodeBlog(data) for data in datas]