import * as util from './util';






function hide() {
    // hide everything exept index
    document.querySelector('#index').display = 'none';
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


function body(category='all', page=1, element_id) {
    const posts = util.get_posts(category, page);
    let elements = [];
    for (let i = 0; i < posts.length; i++) {
        let element = (
            <div class="post">
                <h4>{ posts.body.author }</h4>
                <br></br>
                <p>{ posts.body.message }</p>
            </div>
        );
        elements.push(element);
    }
    ReactDOM(elements, document.querySelector(`#${element_id}`));
    return elements;
}