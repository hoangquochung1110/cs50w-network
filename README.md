# cs50w-network [LIVE DEMO](https://sheltered-chamber-68323.herokuapp.com/)

## My demo of the network project, a Twitter-like social website that allows users to make posts, follow other users, and “like” posts.

## Set up
pre-commit set up
```
pre-commit install
```

## Main features:
* New Post
* All Posts
* Profile Page
* Following: A section that is similar to All Posts section but display only posts made by users that the current user follows.
* Pagination: In any page, there are 10 posts to be display on a page. 
* Edit Post: 
* “Like” and “Unlike”: Users can toggle the "like button" to decide whether they like a post or not. The like count is updated without reloading page
* Filtering (not deployed to prod): Search a certain user by his username

## Key note:
* My app is built on server-first architecture - the most common Django set up. This approach works well for small, simple web app. However, when my web app grows and become complicated, requires doing more complex tasks like managing state, dynamically rendering components, my front-end code slowly expand through your Django templates. You feel it like a chaos, a tangled mess of code. For the next Django project, client-first or hybrid architecture is a goal to accomplish.

* Deployment: It sucks when my apps work well on localhost but it turned out to be ***ERROR 500*** without any useful error message to fix on production server. Should think of new approach (like a new folder structure separating settings_dev.py and settings_prod.py or 2 different branches for dev/prod)
