async function get_posts(category, page_number) {
    const response = await fetch(`get_posts/${category}/${page_number}`);
    const posts = await response.json();
    console.log(posts);
    return posts;
}

