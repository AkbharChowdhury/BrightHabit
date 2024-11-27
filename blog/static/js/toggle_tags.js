window.addEventListener('load', (_) => {
    const chkToggleTags = document.querySelector('#chk_toggle_tags');
    const form = document.querySelector('#blog_search_form');
    if (form && chkToggleTags) {
        chkToggleTags.addEventListener('change', (_) => form.submit())
    }
});
