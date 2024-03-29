



function get_posts(category, page_number) {
    fetch(`get_posts/${category}/${page_number}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
        return posts;
    });
}


