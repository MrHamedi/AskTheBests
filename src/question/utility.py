def like_status_finder(user,post):
    if(user in post.liked_by.all()):
        return("liked")
    elif(user in post.disliked_by.all()):
        return("disliked")
    else:
        return(None)