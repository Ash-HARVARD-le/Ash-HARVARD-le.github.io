// Initialize variables for the game state
let bankValue = parseInt(
  document.getElementById("game-container").dataset.bank, // Get bank value from HTML attribute
  10
);
let currentBet = 0; // The current amount bet by the player
let wager = 5; // The default wager amount
let lastWager = 0; // Store the last wager amount
let bet = []; // Array to track the player's bet
let numbersBet = []; // Array to store the numbers the player has bet on
let previousNumbers = []; // Store previously selected numbers for analysis
let spinInProgress = false; // Flag to prevent multiple spins at once

// Array of red numbers on the roulette wheel
let numRed = [
  1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36,
];

// Array of wheel numbers in the clockwise order
let wheelnumbersAC = [
  0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23,
  8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32,
];

// Create the container for the game
let container = document.createElement("div");
container.setAttribute("id", "container");
document.body.append(container);

// Start the game by building the wheel and betting board
startGame();

// Get references to the wheel and ball track elements
let wheel = document.getElementsByClassName("wheel")[0];
let ballTrack = document.getElementsByClassName("ballTrack")[0];

// Update Users cash, newCash = User's NEW CASH BALANCE
function updateCash(newCash) {
  fetch("/update_cash", {
    method: "POST", // Make a POST request to update the cash value on the server
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ new_cash: newCash }), // Send the new cash value in the request body
  })
    .then((response) => response.json()) // Wait for the server response
    .then((data) => {
      if (data.success) {
        console.log(`Cash updated successfully: ${data.cash}`); // Success
      } else {
        console.error(`Failed to update cash: ${data.error}`); // Failure
      }
    })
    .catch((error) => console.error("Error updating cash:", error));
}

// Starts the game
function startGame() {
  buildWheel();
  buildBettingBoard();
}

// When game is over, prompt user to deposit cash
function gameOver() {
  let notification = document.createElement("div");
  notification.setAttribute("id", "notification");

  // Create a span for the notification message
  let nSpan = document.createElement("span");
  nSpan.setAttribute("class", "nSpan");
  nSpan.innerText =
    "Damn. I was sure you had that too. You know what they say, 100% of gamblers quit before their next big win!";
  notification.append(nSpan);

  // Create a button that leads to /deposit
  let nBtn = document.createElement("div");
  nBtn.setAttribute("class", "nBtn");
  nBtn.innerText = "Deposit Cash Here";
  nBtn.onclick = function () {
    // Redirect the user to the deposit page
    window.location.href = "/deposit";
  };
  notification.append(nBtn);
  container.prepend(notification);
}

// Make the wheel
function buildWheel() {
  // Making the actual wheel
  let wheel = document.createElement("div");
  wheel.setAttribute("class", "wheel");

  let outerRim = document.createElement("div");
  outerRim.setAttribute("class", "outerRim");
  wheel.append(outerRim);

  let numbers = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
  ];

  // Loop through the numbers array to create each section of the wheel
  for (i = 0; i < numbers.length; i++) {
    let a = i + 1;
    let spanClass = numbers[i] < 10 ? "single" : "double";
    let sect = document.createElement("div");
    sect.setAttribute("id", "sect" + a);
    sect.setAttribute("class", "sect");
    let span = document.createElement("span");
    span.setAttribute("class", spanClass);
    span.innerText = numbers[i];
    sect.append(span);
    let block = document.createElement("div");
    block.setAttribute("class", "block");
    sect.append(block);
    wheel.append(sect);
  }

  // Create rim
  let pocketsRim = document.createElement("div");
  pocketsRim.setAttribute("class", "pocketsRim");
  wheel.append(pocketsRim);

  // Create ball track and ball
  let ballTrack = document.createElement("div");
  ballTrack.setAttribute("class", "ballTrack");
  let ball = document.createElement("div");
  ball.setAttribute("class", "ball");
  ballTrack.append(ball);
  wheel.append(ballTrack);

  // Create "pockets" for the ball to land in
  let pockets = document.createElement("div");
  pockets.setAttribute("class", "pockets");
  wheel.append(pockets);

  // Center piece
  let cone = document.createElement("div");
  cone.setAttribute("class", "cone");
  wheel.append(cone);
  let turret = document.createElement("div");
  turret.setAttribute("class", "turret");
  wheel.append(turret);
  let turretHandle = document.createElement("div");
  turretHandle.setAttribute("class", "turretHandle");
  let thendOne = document.createElement("div");
  thendOne.setAttribute("class", "thendOne");
  turretHandle.append(thendOne);
  let thendTwo = document.createElement("div");
  thendTwo.setAttribute("class", "thendTwo");
  turretHandle.append(thendTwo);
  wheel.append(turretHandle);

  container.append(wheel);
}

// Make the betting board
function buildBettingBoard() {
  let bettingBoard = document.createElement("div");
  bettingBoard.setAttribute("id", "betting_board");

  let wl = document.createElement("div");
  wl.setAttribute("class", "winning_lines");

  // Create top section for the first set of bets (double streets)
  var wlttb = document.createElement("div");
  wlttb.setAttribute("id", "wlttb_top");
  wlttb.setAttribute("class", "wlttb");
  for (i = 0; i < 11; i++) {
    let j = i;
    var ttbbetblock = document.createElement("div");
    ttbbetblock.setAttribute("class", "ttbbetblock");
    var numA = 1 + 3 * j;
    var numB = 2 + 3 * j;
    var numC = 3 + 3 * j;
    var numD = 4 + 3 * j;
    var numE = 5 + 3 * j;
    var numF = 6 + 3 * j;
    let num =
      numA +
      ", " +
      numB +
      ", " +
      numC +
      ", " +
      numD +
      ", " +
      numE +
      ", " +
      numF;
    var objType = "double_street";

    // Add event handlers for left click (set bet) and right click (remove bet)
    ttbbetblock.onclick = function () {
      setBet(this, num, objType, 5);
    };
    ttbbetblock.oncontextmenu = function (e) {
      e.preventDefault();
      removeBet(this, num, objType, 5);
    };
    wlttb.append(ttbbetblock);
  }
  wl.append(wlttb);

  // Create second set of bet blocks (split and street bets)
  for (c = 1; c < 4; c++) {
    let d = c;
    var wlttb = document.createElement("div");
    wlttb.setAttribute("id", "wlttb_" + c);
    wlttb.setAttribute("class", "wlttb");
    for (i = 0; i < 12; i++) {
      let j = i;
      var ttbbetblock = document.createElement("div");
      ttbbetblock.setAttribute("class", "ttbbetblock");
      ttbbetblock.onclick = function () {
        if (d == 1 || d == 2) {
          var numA = 2 - (d - 1) + 3 * j;
          var numB = 3 - (d - 1) + 3 * j;
          var num = numA + ", " + numB;
        } else {
          var numA = 1 + 3 * j;
          var numB = 2 + 3 * j;
          var numC = 3 + 3 * j;
          var num = numA + ", " + numB + ", " + numC;
        }
        var objType = d == 3 ? "street" : "split";
        var odd = d == 3 ? 11 : 17;
        setBet(this, num, objType, odd);
      };
      ttbbetblock.oncontextmenu = function (e) {
        e.preventDefault();
        if (d == 1 || d == 2) {
          var numA = 2 - (d - 1) + 3 * j;
          var numB = 3 - (d - 1) + 3 * j;
          var num = numA + ", " + numB;
        } else {
          var numA = 1 + 3 * j;
          var numB = 2 + 3 * j;
          var numC = 3 + 3 * j;
          var num = numA + ", " + numB + ", " + numC;
        }
        var objType = d == 3 ? "street" : "split";
        var odd = d == 3 ? 11 : 17;
        removeBet(this, num, objType, odd);
      };
      wlttb.append(ttbbetblock);
    }
    wl.append(wlttb);
  }

  // Create third set of bet blocks (split bets)
  for (c = 1; c < 12; c++) {
    let d = c;
    var wlrtl = document.createElement("div");
    wlrtl.setAttribute("id", "wlrtl_" + c);
    wlrtl.setAttribute("class", "wlrtl");
    for (i = 1; i < 4; i++) {
      let j = i;
      var rtlbb = document.createElement("div");
      rtlbb.setAttribute("class", "rtlbb" + i);
      var numA = 3 + 3 * (d - 1) - (j - 1);
      var numB = 6 + 3 * (d - 1) - (j - 1);
      let num = numA + ", " + numB;
      rtlbb.onclick = function () {
        setBet(this, num, "split", 17);
      };
      rtlbb.oncontextmenu = function (e) {
        e.preventDefault();
        removeBet(this, num, "split", 17);
      };
      wlrtl.append(rtlbb);
    }
    wl.append(wlrtl);
  }

  // Create corner bet blocks
  for (c = 1; c < 3; c++) {
    var wlcb = document.createElement("div");
    wlcb.setAttribute("id", "wlcb_" + c);
    wlcb.setAttribute("class", "wlcb");
    for (i = 1; i < 12; i++) {
      let count = c == 1 ? i : i + 11;
      var cbbb = document.createElement("div");
      cbbb.setAttribute("id", "cbbb_" + count);
      cbbb.setAttribute("class", "cbbb");
      var numA = "2";
      var numB = "3";
      var numC = "5";
      var numD = "6";
      let num =
        count >= 1 && count < 12
          ? parseInt(numA) +
            (count - 1) * 3 +
            ", " +
            (parseInt(numB) + (count - 1) * 3) +
            ", " +
            (parseInt(numC) + (count - 1) * 3) +
            ", " +
            (parseInt(numD) + (count - 1) * 3)
          : parseInt(numA) -
            1 +
            (count - 12) * 3 +
            ", " +
            (parseInt(numB) - 1 + (count - 12) * 3) +
            ", " +
            (parseInt(numC) - 1 + (count - 12) * 3) +
            ", " +
            (parseInt(numD) - 1 + (count - 12) * 3);
      var objType = "corner_bet";
      cbbb.onclick = function () {
        setBet(this, num, objType, 8);
      };
      cbbb.oncontextmenu = function (e) {
        e.preventDefault();
        removeBet(this, num, objType, 8);
      };
      wlcb.append(cbbb);
    }
    wl.append(wlcb);
  }

  bettingBoard.append(wl);

  // Create the top section of the board (low/high outside bets)
  let bbtop = document.createElement("div");
  bbtop.setAttribute("class", "bbtop");

  // Blocks for "1 to 18" and "19 to 36"
  let bbtopBlocks = ["1 to 18", "19 to 36"];
  for (i = 0; i < bbtopBlocks.length; i++) {
    let f = i;
    var bbtoptwo = document.createElement("div");
    bbtoptwo.setAttribute("class", "bbtoptwo");

    // Define the numbers for each block
    let num =
      f == 0
        ? "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18"
        : "19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36";
    var objType = f == 0 ? "outside_low" : "outside_high";

    // Add event handlers for bets on 1 to 18 and 19 to 36
    bbtoptwo.onclick = function () {
      setBet(this, num, objType, 1);
    };
    bbtoptwo.oncontextmenu = function (e) {
      e.preventDefault();
      removeBet(this, num, objType, 1);
    };
    bbtoptwo.innerText = bbtopBlocks[i];
    bbtop.append(bbtoptwo);
  }
  bettingBoard.append(bbtop);

  // Create the number board (grid of numbers on the roulette table)
  let numberBoard = document.createElement("div");
  numberBoard.setAttribute("class", "number_board");

  // Zero block for the roulette wheel
  let zero = document.createElement("div");
  zero.setAttribute("class", "number_0");
  var objType = "zero";
  var odds = 35;
  zero.onclick = function () {
    setBet(this, "0", objType, odds);
  };
  zero.oncontextmenu = function (e) {
    e.preventDefault();
    removeBet(this, "0", objType, odds);
  };
  let nbnz = document.createElement("div");
  nbnz.setAttribute("class", "nbn");
  nbnz.innerText = "0";
  zero.append(nbnz);
  numberBoard.append(zero);

  // Create blocks for numbered cells on the roulette table
  var numberBlocks = [
    3,
    6,
    9,
    12,
    15,
    18,
    21,
    24,
    27,
    30,
    33,
    36,
    "2 to 1",
    2,
    5,
    8,
    11,
    14,
    17,
    20,
    23,
    26,
    29,
    32,
    35,
    "2 to 1",
    1,
    4,
    7,
    10,
    13,
    16,
    19,
    22,
    25,
    28,
    31,
    34,
    "2 to 1",
  ];
  var redBlocks = [
    1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36,
  ];
  for (i = 0; i < numberBlocks.length; i++) {
    let a = i;
    var nbClass = numberBlocks[i] == "2 to 1" ? "tt1_block" : "number_block";
    var colourClass = redBlocks.includes(numberBlocks[i])
      ? " redNum"
      : nbClass == "number_block"
      ? " blackNum"
      : "";

    // Create each number block
    var numberBlock = document.createElement("div");
    numberBlock.setAttribute("class", nbClass + colourClass);

    // Event handlers for clicking on number blocks
    numberBlock.onclick = function () {
      if (numberBlocks[a] != "2 to 1") {
        setBet(this, "" + numberBlocks[a] + "", "inside_whole", 35);
      } else {
        num =
          a == 12
            ? "3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36"
            : a == 25
            ? "2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35"
            : "1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34";
        setBet(this, num, "outside_column", 2);
      }
    };
    numberBlock.oncontextmenu = function (e) {
      e.preventDefault();
      if (numberBlocks[a] != "2 to 1") {
        removeBet(this, "" + numberBlocks[a] + "", "inside_whole", 35);
      } else {
        num =
          a == 12
            ? "3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36"
            : a == 25
            ? "2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35"
            : "1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34";
        removeBet(this, num, "outside_column", 2);
      }
    };
    var nbn = document.createElement("div");
    nbn.setAttribute("class", "nbn");
    nbn.innerText = numberBlocks[i];
    numberBlock.append(nbn);
    numberBoard.append(numberBlock);
  }
  bettingBoard.append(numberBoard);

  // Create the board for "1 to 12", "13 to 24", "25 to 36" (Dozens)
  let bo3Board = document.createElement("div");
  bo3Board.setAttribute("class", "bo3_board");
  let bo3Blocks = ["1 to 12", "13 to 24", "25 to 36"];
  for (i = 0; i < bo3Blocks.length; i++) {
    let b = i;
    var bo3Block = document.createElement("div");
    bo3Block.setAttribute("class", "bo3_block");
    bo3Block.onclick = function () {
      num =
        b == 0
          ? "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12"
          : b == 1
          ? "13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24"
          : "25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36";
      setBet(this, num, "outside_dozen", 2);
    };
    bo3Block.oncontextmenu = function (e) {
      e.preventDefault();
      num =
        b == 0
          ? "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12"
          : b == 1
          ? "13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24"
          : "25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36";
      removeBet(this, num, "outside_dozen", 2);
    };
    bo3Block.innerText = bo3Blocks[i];
    bo3Board.append(bo3Block);
  }
  bettingBoard.append(bo3Board);

  // Event handler for color/odd/even bets
  let otoBoard = document.createElement("div");
  otoBoard.setAttribute("class", "oto_board");
  let otoBlocks = ["EVEN", "RED", "BLACK", "ODD"];
  for (i = 0; i < otoBlocks.length; i++) {
    let d = i;
    var colourClass =
      otoBlocks[i] == "RED"
        ? " redNum"
        : otoBlocks[i] == "BLACK"
        ? " blackNum"
        : "";
    var otoBlock = document.createElement("div");
    otoBlock.setAttribute("class", "oto_block" + colourClass);
    otoBlock.onclick = function () {
      num =
        d == 0
          ? "2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36"
          : d == 1
          ? "1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36"
          : d == 2
          ? "2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35"
          : "1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35";
      setBet(this, num, "outside_oerb", 1);
    };
    otoBlock.oncontextmenu = function (e) {
      num =
        d == 0
          ? "2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36"
          : d == 1
          ? "1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36"
          : d == 2
          ? "2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35"
          : "1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35";
      e.preventDefault();
      removeBet(this, num, "outside_oerb", 1);
    };
    otoBlock.innerText = otoBlocks[i];
    otoBoard.append(otoBlock);
  }
  bettingBoard.append(otoBoard);

  // Create the chip deck section
  let chipDeck = document.createElement("div");
  chipDeck.setAttribute("class", "chipDeck");

  // Define chip values (1, 5, 10, 100, and "clear" for clearing bets)
  let chipValues = [1, 5, 10, 100, "clear"];

  // Create chips for each value
  for (i = 0; i < chipValues.length; i++) {
    let cvi = i;
    let chipColour =
      i == 0
        ? "red"
        : i == 1
        ? "blue cdChipActive"
        : i == 2
        ? "orange"
        : i == 3
        ? "gold"
        : "clearBet";
    let chip = document.createElement("div");
    chip.setAttribute("class", "cdChip " + chipColour);

    // Event handler for when a chip is clicked
    chip.onclick = function () {
      if (cvi !== 4) {
        // Remove the active class from any previously selected chip
        let cdChipActive = document.getElementsByClassName("cdChipActive");
        for (i = 0; i < cdChipActive.length; i++) {
          cdChipActive[i].classList.remove("cdChipActive");
        }

        // Set the clicked chip as the active chip
        let curClass = this.getAttribute("class");
        if (!curClass.includes("cdChipActive")) {
          this.setAttribute("class", curClass + " cdChipActive");
        }

        // Update wager with the value of the selected chip
        wager = parseInt(chip.childNodes[0].innerText);
      } else {
        // If the "clear" chip is clicked, clear the current bet and update bank value
        bankValue = bankValue + currentBet;
        currentBet = 0;
        document.getElementById("bankSpan").innerText =
          "Cash: " + bankValue.toLocaleString("en-GB") + "";
        document.getElementById("betSpan").innerText =
          "Bet: " + currentBet.toLocaleString("en-GB") + "";
        clearBet(); // Clear any placed bets
        removeChips(); // Remove the chips from the board
      }
    };

    // Create a span for displaying the chip value
    let chipSpan = document.createElement("span");
    chipSpan.setAttribute("class", "cdChipSpan");
    chipSpan.innerText = chipValues[i];
    chip.append(chipSpan);
    chipDeck.append(chip);
  }
  bettingBoard.append(chipDeck);

  // Create the bank container
  let bankContainer = document.createElement("div");
  bankContainer.setAttribute("class", "bankContainer");

  // Create the bank section to display the player's available cash
  let bank = document.createElement("div");
  bank.setAttribute("class", "bank");
  let bankSpan = document.createElement("span");
  bankSpan.setAttribute("id", "bankSpan");
  bankSpan.innerText = "Cash: " + bankValue.toLocaleString("en-GB") + "";
  bank.append(bankSpan);
  bankContainer.append(bank);

  // Create the bet section to display the current bet value
  let bet = document.createElement("div");
  bet.setAttribute("class", "bet");
  let betSpan = document.createElement("span");
  betSpan.setAttribute("id", "betSpan");
  betSpan.innerText = "Bet: " + currentBet.toLocaleString("en-GB") + "";
  bet.append(betSpan);
  bankContainer.append(bet);
  bettingBoard.append(bankContainer);

  let pnBlock = document.createElement("div");
  pnBlock.setAttribute("class", "pnBlock");
  bettingBoard.append(pnBlock);

  container.append(bettingBoard);
}

// Clears all bets and resets the bet and number arrays
function clearBet() {
  bet = [];
  numbersBet = [];
}

// Sets a new bet, adjusting the wager and updating the UI accordingly
function setBet(e, n, t, o) {
  lastWager = wager;
  wager = bankValue < wager ? bankValue : wager; // Ensure the wager doesn't exceed bank value
  if (wager > 0) {
    // Add a spin button if it doesn't already exist
    if (!container.querySelector(".spinBtn")) {
      let spinBtn = document.createElement("div");
      spinBtn.setAttribute("class", "spinBtn");
      spinBtn.innerText = "spin";
      spinBtn.onclick = function () {
        this.remove(); // Remove the spin button when clicked
        spin();
      };
      container.append(spinBtn);
    }

    // Adjust bank and current bet values
    bankValue = bankValue - wager;
    currentBet = currentBet + wager;
    document.getElementById("bankSpan").innerText =
      "Cash: " + bankValue.toLocaleString("en-GB") + "";
    document.getElementById("betSpan").innerText =
      "Bet: " + currentBet.toLocaleString("en-GB") + "";

    // Check if the bet already exists and update it
    for (i = 0; i < bet.length; i++) {
      if (bet[i].numbers == n && bet[i].type == t) {
        bet[i].amt = bet[i].amt + wager; // Add the wager to the existing bet
        let chipColour =
          bet[i].amt < 5
            ? "red"
            : bet[i].amt < 10
            ? "blue"
            : bet[i].amt < 100
            ? "orange"
            : "gold";
        e.querySelector(".chip").style.cssText = "";
        e.querySelector(".chip").setAttribute("class", "chip " + chipColour);
        let chipSpan = e.querySelector(".chipSpan");
        chipSpan.innerText = bet[i].amt;
        return;
      }
    }

    // Create a new bet entry
    var obj = {
      amt: wager,
      type: t,
      odds: o,
      numbers: n,
    };
    bet.push(obj);

    // Add the numbers to the numbersBet array
    let numArray = n.split(",").map(Number);
    for (i = 0; i < numArray.length; i++) {
      if (!numbersBet.includes(numArray[i])) {
        numbersBet.push(numArray[i]);
      }
    }

    // Create the chip element for the new bet
    if (!e.querySelector(".chip")) {
      let chipColour =
        wager < 5
          ? "red"
          : wager < 10
          ? "blue"
          : wager < 100
          ? "orange"
          : "gold";
      let chip = document.createElement("div");
      chip.setAttribute("class", "chip " + chipColour);
      let chipSpan = document.createElement("span");
      chipSpan.setAttribute("class", "chipSpan");
      chipSpan.innerText = wager;
      chip.append(chipSpan);
      e.append(chip);
    }
  }
}

// Executes the spin logic and handles the outcome (win, lose, tie)
function spin() {
  spinInProgress = true;
  var winningSpin = Math.floor(Math.random() * 37); // Random spin result between 0 and 36
  spinWheel(winningSpin); // Call the wheel rotation function

  // Delay the results processing
  setTimeout(function () {
    let totalBet = 0;
    let winValue = 0;
    let betTotal = 0;
    let result = "Lose"; // Default result

    for (i = 0; i < bet.length; i++) {
      totalBet += bet[i].amt; // Accumulate total bet
    }

    // Check if any bets are winning
    if (numbersBet.includes(winningSpin)) {
      // Loop through all the bets to calculate winnings and total bet
      for (i = 0; i < bet.length; i++) {
        var numArray = bet[i].numbers.split(",").map(Number);
        if (numArray.includes(winningSpin)) {
          bankValue = bankValue + bet[i].odds * bet[i].amt + bet[i].amt; // Calculate new bank balance
          winValue = winValue + bet[i].odds * bet[i].amt; // Calculate winnings
          betTotal = betTotal + bet[i].amt; // // Calculate total bet amount
        }
      }
      // Determine the result (win, tie, lose)
      if (winValue + betTotal > totalBet) {
        result = "Win";
      } else if (winValue + betTotal === totalBet) {
        result = "Tie";
      } else {
        result = "Lose";
      }
      win(winningSpin, winValue, betTotal, totalBet);
    }

    // Send game statistics to the server
    fetch("/update_game_stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        bet: totalBet, // Total amount bet by the user
        result: result, // Result of the spin (Win, Tie, Lose)
      }),
    });

    // Update UI with final results
    document.getElementById("bankSpan").innerText =
      "Cash: " + bankValue.toLocaleString("en-GB") + "";
    updateCash(bankValue);
    currentBet = 0;
    bet = [];
    numbersBet = [];
    removeChips();

    document.getElementById("betSpan").innerText =
      "Bet: " + currentBet.toLocaleString("en-GB") + "";

    let pnClass = numRed.includes(winningSpin)
      ? "pnRed"
      : winningSpin == 0
      ? "pnGreen"
      : "pnBlack";
    let pnContent = document.getElementById("pnContent");
    let pnSpan = document.createElement("span");
    pnSpan.setAttribute("class", pnClass);
    pnSpan.innerText = winningSpin;
    pnContent.append(pnSpan);
    pnContent.scrollLeft = pnContent.scrollWidth;

    wager = lastWager; // Reset the wager for the next spin

    // Check if player can continue, otherwise, gameOver (which just asks them to deposit more money)
    if (bankValue == 0 && currentBet == 0) {
      gameOver();
    }
  }, 10000);
  spinInProgress = false;
}

// Displays a win notification
function win(winningSpin, winValue, betTotal, totalBet) {
  if (winValue > 0) {
    let notification = document.createElement("div");
    notification.setAttribute("id", "notification");
    let nSpan = document.createElement("div");
    nSpan.setAttribute("class", "nSpan");
    let nsnumber = document.createElement("span");
    nsnumber.setAttribute("class", "nsnumber");
    nsnumber.style.cssText = numRed.includes(winningSpin)
      ? "color:red"
      : "color:black";
    nsnumber.innerText = winningSpin;
    nSpan.append(nsnumber);
    let nsTxt = document.createElement("span");
    nsTxt.innerText = " Win";
    nSpan.append(nsTxt);
    let nsWin = document.createElement("div");
    nsWin.setAttribute("class", "nsWin");
    let nsWinBlock = document.createElement("div");
    nsWinBlock.setAttribute("class", "nsWinBlock");
    nsWinBlock.innerText = "Bet: " + totalBet;
    nSpan.append(nsWinBlock);
    nsWin.append(nsWinBlock);
    nsWinBlock = document.createElement("div");
    nsWinBlock.setAttribute("class", "nsWinBlock");
    nsWinBlock.innerText = "Win: " + winValue;
    nSpan.append(nsWinBlock);
    nsWin.append(nsWinBlock);
    nsWinBlock = document.createElement("div");
    nsWinBlock.setAttribute("class", "nsWinBlock");
    nsWinBlock.innerText = "Payout: " + (winValue + betTotal);
    nsWin.append(nsWinBlock);
    nSpan.append(nsWin);
    notification.append(nSpan);
    container.prepend(notification);
    setTimeout(function () {
      notification.style.cssText = "opacity:0";
    }, 3000);
    setTimeout(function () {
      notification.remove();
    }, 4000);
  }
}

// Removes a specific bet and updates the game state
function removeBet(e, n, t, o) {
  wager = wager == 0 ? 100 : wager;
  for (i = 0; i < bet.length; i++) {
    if (bet[i].numbers == n && bet[i].type == t) {
      if (bet[i].amt != 0) {
        wager = bet[i].amt > wager ? wager : bet[i].amt;
        bet[i].amt = bet[i].amt - wager;
        bankValue = bankValue + wager;
        currentBet = currentBet - wager;
        document.getElementById("bankSpan").innerText =
          "Cash: " + bankValue.toLocaleString("en-GB") + "";
        document.getElementById("betSpan").innerText =
          "Bet: " + currentBet.toLocaleString("en-GB") + "";
        if (bet[i].amt == 0) {
          e.querySelector(".chip").style.cssText = "display:none";
        } else {
          let chipColour =
            bet[i].amt < 5
              ? "red"
              : bet[i].amt < 10
              ? "blue"
              : bet[i].amt < 100
              ? "orange"
              : "gold";
          e.querySelector(".chip").setAttribute("class", "chip " + chipColour);
          let chipSpan = e.querySelector(".chipSpan");
          chipSpan.innerText = bet[i].amt;
        }
      }
    }
  }

  // Remove the spin button if there are no active bets
  if (currentBet == 0 && container.querySelector(".spinBtn")) {
    document.getElementsByClassName("spinBtn")[0].remove();
  }
}

// Animates the wheel and ball for the spin result
function spinWheel(winningSpin) {
  for (i = 0; i < wheelnumbersAC.length; i++) {
    if (wheelnumbersAC[i] == winningSpin) {
      var degree = i * 9.73 + 362;
    }
  }

  wheel.style.cssText = "animation: wheelRotate 5s linear infinite;";
  ballTrack.style.cssText = "animation: ballRotate 1s linear infinite;";

  setTimeout(function () {
    ballTrack.style.cssText = "animation: ballRotate 2s linear infinite;";
    style = document.createElement("style");
    style.type = "text/css";
    style.innerText =
      "@keyframes ballStop {from {transform: rotate(0deg);}to{transform: rotate(-" +
      degree +
      "deg);}}";
    document.head.appendChild(style);
  }, 2000);
  setTimeout(function () {
    ballTrack.style.cssText = "animation: ballStop 3s linear;";
  }, 6000);
  setTimeout(function () {
    ballTrack.style.cssText = "transform: rotate(-" + degree + "deg);";
  }, 9000);
  setTimeout(function () {
    wheel.style.cssText = "";
    style.remove();
  }, 10000);
}

// Removes all chips from the screen
function removeChips() {
  var chips = document.getElementsByClassName("chip");
  console.log("Chips before removal: ", chips.length); // Log the number of chips before removal
  while (chips.length > 0) {
    console.log("Removing chip:", chips[0]); // Log the chip being removed
    chips[0].remove(); // Remove the first chip in the list
  }
  console.log("Chips after removal: ", chips.length); // Log to verify if all chips were removed
}
