const numPosts = parseInt(document.getElementById('num_posts').getAttribute('value'));
const rank = document.getElementById('rank');
rank.style.color = getRankColour(numPosts);
// const progressBar = document.getElementById('progress-bar');
const details = rankDetails()
// const isBronze = details.bronze.isBronze(11)
// console.log({isBronze})

function constructProgressBar() {
    const progressBar = document.querySelector('#rank_progressbar');
    const per = 75;
    const status = 'only 2 more to posts to go till you reach silver'

    progressBar.style.background = '#CE8946';
    progressBar.style.width = `${per}%`;
    progressBar.innerText = `${per}% ${status}`;
    progressBar.setAttribute('aria-valuenow', per);
}

function getRankColour(numPost = 0) {
    const ranks = rankDetails();

    if (ranks.bronze.hasQualified(numPosts)) {
        return ranks.bronze.colour;
    }
    if (ranks.silver.hasQualified(numPosts)) {
        return ranks.silver.colour;
    }
    return ranks.gold.colour;

}

function rankDetails() {
    return {

        'bronze': {
            'colour': '#CE8946',
            'num': 5,
            hasQualified: function (numPosts) {
                return numPosts <= this.num;

            }
        },


        'silver': {
            'colour': '#C0C0C0',
            'num': 10,
            hasQualified: function (numPosts) {
                return numPosts <= this.num;

            }
        },


        'gold': {
            'colour': '#FFD700',
            'num': 11
        },

    }
}