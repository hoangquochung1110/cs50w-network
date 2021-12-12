# cs50w-network [LIVE DEMO](https://sheltered-chamber-68323.herokuapp.com/)

## My demo of the network project, a Twitter-like social website that allows users to make posts, follow other users, and “like” posts.

## Main features:
* New Post: Users who signed in are able to write a 200-character post filling in text into a form.
* All Posts: A section in which any user can see all posts from all users. 
* Profile Page: To show some basic data on an user such as: username, first name, last name, number of posts/followers/following.
* Following: A section that is similar to All Posts section but display only posts made by users that the current user follows.
* Pagination: In any page, there are 10 posts to be display on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts and  posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.
* Edit Post: Users are able to edit their own posts. The new content of the post should be updated without reloading page.
* “Like” and “Unlike”: Users can toggle the "like button" to decide whether they like a post or not. The like count is updated without reloading page
* Filtering (not deployed to prod): Search a certain user by his username

## Key note:
My app is built on server-first architecture - the most common Django set up. This approach works well for small, simple web app. However, when my web app grows and become complicated, requires doing more complex tasks like managing state, dynamically rendering components, my front-end code slowly expand through your Django templates. You feel it like a chaos, a tangled mess of code. For the next Django project, client-first or hybrid architecture is a goal to accomplish.
