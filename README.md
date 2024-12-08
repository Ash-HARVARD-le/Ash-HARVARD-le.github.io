<h1> Harvard Gambling Mania </h1>

<h2> Welcome to Harvard Gambling Mania (HGM)! </h2>

<p> Do you have what it takes to become the best gambler at Harvard? I have created this interactive website that allows users to play casino-like games, such as blackjack, roulette, and a slot machine. First you are required to sign up, and you get a $100 incentive to begin gambling once logging in. If you lose it all (what a terrible gambler you are), but don't fret, because in the Account page you can deposit more money into your account and gamble larger bets! They do require you to sign up with your HUID or Credit Card Information, so they should really be used as a last resort. Additionally, you are able to update your password, delete your account, view your game statistics, and even check if you're on the leaderboard! This website is meant to be for entertainment purposes only, and the gambles are not with real money, but with Malanion dollars. Please enjoy! </p>

<a href="https://youtu.be/V8NA9QzBmHE?si=kKjpfwW0AMkDqURW"> Click Here to view the website in action! </a>

<h3> Games: </h3>
<ul>
<li>Blackjack</li>
<li>Roulette</li>
<li>Slot Machine</li>
</ul>

<h3> Features: </h3>
<ul>
<li>Leaderboard</li>
<li>Game Statistics</li>
<li>Update Password</li>
<li>Deposit Money (HUID & Credit)</li>
<li>Delete Account</li>
</ul>

<h2>Setup:</h2>
<p>To run the project, make sure you have the following installed on your computer:</p>

<ol>
<li>Python 3 (must download on your laptop first)</li>
<li>Flask (Terminal in VSCode: pip install flask)</li>
<li>Flask-login (Terminal in VSCode: pip install flask-login)</li>
<li>SQLAlchemy (Terminal in VSCode: pip install flask-sqlalchemy)</lii>
</ol>

<br />

<p> What else is used? </p>
<ul>
<li>HTML</li>
<li>CSS</li>
<li>JavaScript</li>
</ul>

<h3> How to run the program? </h3>
<p> In the main.py you will want to run a python file and the website (local) link should be shown in the terminal </p>

<h2>Blackjack</h2>
<p>The first game we have is Blackjack, and the game is quite simple. If you don't know the rules, search it up, it's not hard (just get to 21). To play, simply enter a valid bet amount and press the green button to start the round. If you leave the site in the middle of a game by accident, DON'T WORRY, just head back to the page and the game will pick up where you left off. Although, if you log out, don't expect to see that game anymore, and your bets will be lost. Once you get your cards, you have two options, Hit or Stand. Based on the cards you have, you have to be strategic, as you only know one of the dealer's cards. Click the hit button to get another card, but be careful because you could bust. Click the stand button to end your turn and allow the dealer to play theirs. It isn't rigged I promise, the results are shown after each round. Your cash increases if you win the bet, it stays the same if you have the same value cards as the dealer, but you lose money if, well, you lose. But you're a great gambler so I am sure you won't lose. Anyways, once the game ends, you will be told exactly how much you won, and you can place another bet to start the game again. Happy Blackjack! </p>

<h2>Roulette</h2>
<p>The second game we have is Roulette, and the game is also quite simple. If you don't know the rules, search it up, it's not hard (just place random bets and spin). To play, simply click on the chips on the bottom left of the screen and place them (preferably on the text of the whatever bet you want on the betting table) and then press the yellow "Spin" button that appears when you successfully place a bet in order to start a round. If you leave the site in the middle of a game by accident, then the game does not continue and you will not win, lose, or tie (you could've missed out on millions). After you spin, you simply wait a few seconds before the ball locks in on a pocket and you get to know how much you bet and how much you won, only if you actually win. Otherwise, you just lost all of the bets you placed on the spin and you're just bad. This game is entirely luck based, so, do you have the luck? Similarly to Blackjack, it isn't rigged, and I think it would've been tougher to rig it than to just be honest with the code. Additionally, your cash increases if you win the bet, it stays the same if you end up winning the same amount you bet, but you lose money if, well, you lose. You can also see the amount of cash you have on the bottom left corner of the screen (underneath the chips) to let you know if you have enough to bet. Automatically, if you place chips on bets where you do not have enough money, it will prevent you from doing so since you don't have the funds. To remove a bet (let's say you accidentally clicked a wong bet you didn't want), simply right click the bet you placed or go to the bottom left red button and clear ALL bets. The text box on the right of where it displays your money is the current bet amount you have placed across all bets on this roulette spin. Anyways, once the game ends, if you won, you will be told exactly how much you won, and you can place another bet to start the game again. Happy Roulette! </p>

<h2>Slot Machine</h2>
<p>The last game we have is the Slot Machine, and the game is the simplest out of all previous ones. The only rule is clicking the bet and spin button and hope you get a winning spin. The default cost per spin is 1$, however, if you have more than $100, then the stakes increase and each spin will result in a 1% cost of your total cash. This way there is always a risk and an even higher reward for larger bets. Upon clicking the button, the slot machine will randomly pick (out of 9 images) the one the gambling gods want and if you lose, then you lose money and the slot machine will turn red to let you know. You will also be given an encouraging message to continue on with your gambling career. If you win, (basically if you match at least 2, you get 2x your bet, if your match any important 2 (horseshoe, diamond, 7, bar), then you actually get 10x your bet, if you match all 3 you get 50x your bet, and if you match all 3 for any important icon, you get 500x the cost for a spin), then you win money. If you win, you get your money updated, the slot machine turns green, and you're told how much you won! If you leave the site in the middle of a game by accident, WORRY, because that bet is gone. This also isn't rigged I promise. It is possible to win (it's even possible to win the 500x, I've gotten it only once). Your cash increases if you win the bet, you lose your money otherwise. Once the game ends, the button will return to normal and you can place another bet to start the game again. Happy Slots!</p>

<h1>Other features</h1>

<h2>Leaderboard</h2>
<p>
The leaderboard displays the top gamblers and their earnings. It ranks players based on their total winnings (total win amount - total loss amount), NOT on their total cash:
<ul>
  <li><strong>Gold</strong>: Awarded to the best gambler</li>
  <li><strong>Silver</strong>: Awarded to the second best gambler</li>
  <li><strong>Bronze</strong>: Awarded to the third best gambler</li>
  <li><strong>Red</strong>: Awarded to the 4th place players and below</li>
</ul>
This feature is great because you can compete with others and try to be the best gambler, so aim for higher rankings and prove your the best!
</p>

<h2>Your Game Statistics</h2>
<p>
In the records page, pretty much any details on your gambling history is here, if you just started, nothing is shown. The following is shown
<ul>
  <li>Number of games played</li>
  <li>Wins ($ made from gambling and your largest bet won) and losses ($ lost and largest bet lost)</li>
  <li>Favorite and least favorite games based on how many times you've played it</li>
  <li>Luckiest and unluckiest games based on your win and loss record</li>
  <li>Inidividual wins, ties (if applicable), losses for each game</li>
</ul>
The stats update after every game played, so it's helpful to view which games you're best at.
</p>

<h2>Update Password</h2>
<p>
For security purposes, users can update their account passwords. To do so:
<ol>
  <li>Navigate to the Account page and the "Update Password" section.</li>
  <li>Click the button and then you're prompted to enter your current username and password for verification.</li>
  <li>Input and confirm your new password.</li>
  <li>Click "Update Password" to save changes.</li>
</ol>
The system logs you out and you're prompted to sign in again after your changes are complete.
</p>

<h2>Deposit Money (Credit vs HUID)</h2>
<p>
Users can deposit money into their accounts using two methods:
<ul>
  <li><strong>Credit:</strong> Direct deposits made through a credit card.</li>
  <li><strong>HUID:</strong> Secure transactions through an HUID (can't change after you submit to ensure security).</li>
</ul>
Deposited funds are reflected in your account balance and can be used for gameplay. Additionally, show and hide buttons have been provided to allow you to recheck your input information.
</p>

<h2>Delete Account</h2>
<p>
After registering, if a user wishes to stop using the platform, they can log out or delete their account. Logging out simply logs the user, out, but deleting their account means the following:
<ul>
  <li>All user data from the system will be deleted. The user, username/password, and personal/sensitive information</li>
  <li>Additionally, gameplay history for that user will be deleted as well as their account balance.</li>
</ul>
To delete your account, navigate to the "Delete Account" section in the account page, confirm your decision (which you are prompted to do since this is a dangerous action), and click "Confirm" to delete your account. Note: This action is irreversible.
</p>

<h1> Who contributed to this project? </h1>
<p> Making this by myself in the span of two weeks is a crazy task. Especially when you have other things to accomplish within that time. That's why I would love to thank a couple of people who contributed (albeit they will never know they helped me so much) in making this website.</p>

<h3>Tech with Tim: https://youtu.be/dam0GPOAvVI?si=GHrqd9_vQq8d2Lix</h3>
<p>My GOAT who helped me set up flask, authentication, and databases with SQLAlchemy</p>

<h3>API: https://deckofcardsapi.com</h3>
<p>My GOAT who provided me with an API to use for the cards in blackjack</p>

<h3>milsaware: https://github.com/milsaware/javascript-roulette?tab=readme-ov-file</h3>
<p>My GOAT on github who provided some extremely useful javascript and html for the base of my roulette game. Thankfully they are totally chill with allowing me to edit it for private use as mentioned in their copyright bio.
</p>

<h3>Web Contaent: https://youtu.be/0JYFFay6GO8?si=EVsRuozhF1DFviV5</h3>
<p>MY LAST GOAT ON YOUTUBE who helped me with the base javascript and css to handle a slot machine game!!!</p>
