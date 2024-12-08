<h1>Harvard Gambling Mania (HGM) - Design </h1>

<p>The following content involves the design choices I made while developing Harvard Gambling Mania. The web application was built using Flask, JavaScript, and CSS for an interactive, responsive, and user-friendly experience.</p>

<h2>Backend - Flask</h2>
<p>Flask serves as the backend of the application.</p>

<strong>Routes</strong>:

<p>Routes in auth.py render dynamic pages that deal with more about the personal information of the user (registering, logging in, depositing, and any stuff in the account page). This is because I wanted to keep it separate from views.py, since auth.py needs more seucirty. Routes in views.py deal less with security measures and allow user to access pages like the actual games, user's account, and the leaderboard. All these routes (except for registering and logging in) are not available to the user if they have not registered an account. These pages utilize HTML for the frontend design, SQLAlchemy to store and display user gambling information, and Javascript for some visuals and actual workings of some games. Once logged in, they lose access those links and have another one that logs them out instead. This is because these features make logical sense to include. Additionally, any errors or mistakes on our or user's behalf leads them to a beautiful apology page. 
</p>

<strong>Games</strong>:

<p>Each game and their logic (if not already using javascript) is implemented here and is used to dynamically display their cards, or their cash, or receive and send information to javascript to display accurate cash amounts, update them, and store games into the database. For blackjack, some cool design options is that cards are actually shown because flask utilizes an card deck API to run the game. When receiving a bet, it begins the game on the same page, displays the cards, and only displays 1 of the dealers cards which makes sense, since you should be able to see 1 and not see 1 at the beginning. Different buttons for hitting and standing which lead to different things happening, like hitting gives you another card, standing means you end your turn. Then the result and amount won is passed over to the frontend to display this information and stores the game into the GameStats database. Additionally, to prove that the game is not rigged, I ensured that the cards from the previous round are displayed underneat the results so the user can see for themself the game was played out accordingly. For roulette, it mainly used javascript, however flask and javascript communicated to update the user's cash and add a game to the GameStats database. Additionally, slots also uses javascript for the interactive features of the game but uses flask to update the users cash and store game in database, then it communicates with javascript to let the user know how much they won. </p>

<h2>Frontend - HTML, CSS, JavaScript</h2>

<ol>
<li>
<strong>HTML</strong>: The HTML structure is straightforward, I use jinja which uses layout.html as the base template and each page has their own body. This is to be organized and clear, additionally, I ensure there is input fields, buttons, sections that display the games, sections to display the leaderboard, a page to show different images and work with flask to utilize the GameStats database (display gambling records), and an account page to work with more features dealing with their account. Each section is displayed dynamically based on the current user that is using the website, their cash, and their gambling information. One more thing to mention is the use of dynamic max inputs for input fields, since a user can't input a larget value than they currently have.
</li>
<br/>
<li>
<strong>CSS / Bootstrap</strong>: Custom styles are applied to ensure a visually appealing user interface. Key aspects
include:
<ul>
<li>Flexbox for centering and responsive layouts (I like things centered)</li>
<li>Casino-like background color (To make it feel like you're really in one)</li>
<li>Dynamic leaderboard rankings with color-coded ranks (help distinguish the good gamblers from the bad)</li>
<li>Multi-colored logo</li>
<li>Reasonably sized images</li>
<li>Roulette page with the betting table, chip location, and wheel location</li>
<li>Slot machine display and design like (position, coloring for wins/losses, and text size)</li>
</ul>
The goal of the CSS design was to create an immersive "casino" feel for the user and make the games look actually nice.
</li>
<br/>
<li>
<strong>JavaScript</strong>: Javascript was used a lot to dynamically change the width of input fields based on the length of placeholders (involved user's cash), as well as the roulette and slot machine games. The javascript was used to spin wheels or reels of the game, and were used to dynamically display the user's current cash, keep track of bets, display the games, display winning/losing messages, and redirect to the deposit page if necessary. Machine's and wheel spinning animation and random outcomes are managed by JavaScript. It communicates with the Flask backend to retrieve data such as win/loss results and updates the game state in real-time.
</li>
</ol>

<h2>Design Decisions</h2>
<ul>
<li> Navigation bar for easy access to different web links across all pages</li>
<li>Casino Backgruond color so it feels like one</li>
<li> Images for each game that lead to their respective games</li>
<li>Register and log in before you can access any features</li>
<li>Apology page with AMOGUS because I thought it would be funny</li>
<li>Clickable logo to go back to home</li>
<li>Dealer face down card in blackjack</li>
<li>Can't bet more than your current cash</li>
<li>Input form disappears while in the middle of a game</li>
<li>Visible cards</li>
<li>Display previous games results in blackjack</li>
<li>Display amount won in blackjack</li>
<li>Display roulette wheel and betting table</li>
<li>Random every time a spin is done so not rigged</li>
<li>When clicking a chip, it gets bigger so you know which chip is activated</li>
<li>Display user cash</li>
<li>Display working chips to bet</li>
<li>Roulette wheel actually spins</li>
<li>Right click to clear a bet</li>
<li>Spin button appears only after you place a bet</li>
<li>Display the slot machine (3 different reels)</li>
<li>Random every time a spin is done so it's not rigged</li>
<li>Place bet and spin button deactivates while in the middle of a spin and reactivates later</li>
<li>Images change at different speeds</li>
<li>Different payouts based on the images that appear</li>
<li>Display cash and win amount</li>
<li>Turn slot machine green if there was a win to show the user won and they recognize it, red if they lose a bet (resets after every spin)</li>
<li>Background is green but leaderBOARD is white to contrast and display the different rank color of users</li>
<li>Gold for 1st, Silver 2nd, Bronze 3rd, Red for below</li>
<li>When hovering, the background gets slightly darker for each rank</li>
<li>Differnet images to go along with different stats (funny images)</li>
<li>Welcome the user with their username</li>
<li>Win information goes together, loss information goes together, favorite/least favorite, luck/unlucky</li>
<li>Image generated based on the actual game stat</li>
<li>Display percentage of wins/losses</li>
<li>Individual game stats for each user so they can view clearer</li>
<li>Separated into 3 different cards for easier view</li>
<li>Simple account page</li>
<li>Different color buttons to match the action (delete is danger, deposit is green cuz money, and blue for password because it's a mediocre action)</li>
<li>Display username for welcoming feel and cash for effective view to see after you deposit. </li>
<li>Compatible with phones/smaller screens</li>
</ul>
