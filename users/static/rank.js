const ranks = rankDetails();
const numPosts = parseInt(document.getElementById('num_posts').getAttribute('value'))
const rank = document.getElementById('rank');
rank.style.color = getRankColour(numPosts);
const details = rankDetails()

function percentage(partialValue, totalValue) {
    return (100 * partialValue) / totalValue;
}
console.log({numPosts})
constructProgressBar(numPosts)
function constructProgressBar(numPosts) {
    if (numPosts >= details.gold.num) {
        document.getElementById('rank_section').style.display = 'none'
        return
    }

    const progressBar = document.querySelector('#rank_progressbar');
    const rankNumber = getRankNumber(numPosts);
    const percentagePosts = percentage(numPosts, rankNumber);

    const numLeftTillNextRank =  (rankNumber+1) - numPosts
    const message = `only ${numLeftTillNextRank} more to posts to go till you reach ${nextRank()}`
    progressBar.style.background = getRankColour(numPosts);
    progressBar.style.width = `${percentagePosts}%`;
    progressBar.innerText = `${percentagePosts}%`;
    document.getElementById('message').innerText = message
    progressBar.setAttribute('aria-valuenow', percentagePosts);
}

function getRankColour(numPost = 0) {

    if (ranks.bronze.hasQualified(numPosts)) {
        return ranks.bronze.colour;
    }
    if (ranks.silver.hasQualified(numPosts)) {
        return ranks.silver.colour;
    }
    return ranks.gold.colour;

}

function getRankNumber() {
    if (ranks.bronze.hasQualified(numPosts)) {
        return ranks.bronze.num;
    }
    if (ranks.silver.hasQualified(numPosts)) {
        return ranks.silver.num;
    }
    return ranks.gold.num;

}


function nextRank() {
    if (ranks.bronze.hasQualified(numPosts)) {
        if (ranks.silver.hasQualified(numPosts)) {
            return 'silver'
        }

    }
    return 'gold'


}

function rankDetails() {
    return Object.freeze(
        {

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
    );
}