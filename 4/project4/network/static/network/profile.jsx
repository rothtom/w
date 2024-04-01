if (document.readyState !== 'loading') {
    profile();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        profile();
    });
}


function profile() {
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

    toggle_button_disabled();

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