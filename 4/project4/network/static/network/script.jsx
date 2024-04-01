if (document.readyState !== 'loading') {
    index();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        index();
    });
}




function index() {
    history.pushState({'page': 1, 'category': 'all', 'element_id': 'all_posts'}, '', `/posts/all/1`);
    window.onpopstate = function (event) {
        body({category: event.state.category, page: event.state.page, element_id: event.state.element_id});
    }
    ReactDOM.render(new_post_form(), document.querySelector('#new_post'));
    document.querySelector('#post_new_post').onclick = post_new_post;
    body({element_id: 'all_posts'});
}




function hide(element_ids) {
    // hide everything exept index
    for (let i = 0; i < element_ids.length; i++){
        document.querySelector(`#${element_ids[i]}`).display = 'none';
    }
}




function show(element_ids) {
    // hide everything exept index
    for (let i = 0; i < element_ids.length; i++){
        document.querySelector(element_ids[i]).display = 'block';
    }
}









function new_post_form() {
    const new_post_form = (
        <div class="post">
            <h4>New Post:</h4>
            <textarea type="text" name="message" rows="4" cols="200" id="new_post_message"></textarea>
            <br></br>
            <button id="post_new_post">Post!</button>
        </div>  
    );
    return new_post_form;
}


function post_new_post() {
    let message = document.querySelector('#new_post_message').value;
    document.querySelector('#new_post_message').value = '';
    console.log(`new post message: ${message}`);
    fetch('/create_post', {
        method: 'POST',
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(result => 
        console.log(result)
    );
    return 0;
}





function body({category='all', page=1, element_id}) {
    const posts = get_posts(category, page).then(posts => {
        console.log(posts);
        let elements = [];
        for (let i = 0; i < posts.body.length; i++) {

            let element = (
                <div class="post">
                    <a href={ "/profile/" + posts.body[i].author }><h4>{ posts.body[i].author }</h4></a>
                    <br></br>
                    <p>{ posts.body[i].message }</p>
                </div>
            );
            elements.push(element);
        }
        ReactDOM.render(elements, document.querySelector(`#${element_id}`));
        let options = [];
        for (let i = 1; i <= posts.context.page_count; i++) {
            const option = (
                <option value={ i }>{ i }</option>
            );
            options.push(option);
        }
        ReactDOM.render(options, document.querySelector('#page_selector'));

         //change button clickability
        toggle_button_disabled(posts.context);


        history.pushState({'page': page, 'category': category, 'element_id': element_id}, '', `/posts/${category}/${page}`);
    });

    document.querySelector('#page_selector').addEventListener('change', () => {
        body({category: history.state.category, page: history.state.page, element_id: history.state.element_id});
    });

   



    document.querySelectorAll('.pageflip_button').forEach(button => {
        button.onclick = (button, event) => {
            const current_page = parseInt(document.querySelector('#page_selector').value);
            let page = 0;
            if (button.target.dataset.direction === 'next') {
                page = current_page + 1;
            } else {
                page = current_page - 1;
            }
            console.log(page)
            document.querySelector('#page_selector').value = page;
            body({category: history.state.category, page: page, element_id: history.state.element_id});
        }
    });
}



async function get_posts(category, page_number) {
    const response = await fetch(`/get_posts/${category}/${page_number}`);
    const posts = await response.json();
    console.log(posts.message);
    return posts;
}


function toggle_button_disabled(context) {
    const back = document.querySelector('#flip_back');
    const next = document.querySelector('#flip_next');

    if (context.has_next) {
        next.disabled = false;
    } else {
        next.disabled = true;
    }

    if (context.has_previous) {
        back.disabled = false;
    } else {
        back.disabled = true;
    }
}


async function profile(username) {
    hide("index", "following");
    show("profile");
    const response = await fetch(`/profile/${username}`);
    console.log(response);
    const profile = await response.json();
    console.log(profile);
    let profile_info = (
        <div class="profile" id="profile-info">
            <h1>{ profile.body.username }</h1>
            <div calss="profile_stats" id="profile_stats">
                <div>
                    <p>Follower(s) { profile.body.followers }</p>
                    <p>Following: { profile.body.following }</p>
                    <button id="follow_button" display="none">{ follow }</button>
                </div>
            </div>
        </div>
    );
    ReactDOM.render(profile_info, document.querySelector('#profile'))
    
    if (profile.logged_in) {
        document.querySelector('#follow_button').display = block;
    }
}
       