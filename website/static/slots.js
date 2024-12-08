const handleButton = document.getElementById("handle");
const reels = document.querySelectorAll(".reel");
const slots_message = document.getElementById("slots_message");
const slotMachine = document.querySelector(".slot-machine");

// images
const images = [
  "/static/slot_icons/bar.jpg",
  "/static/slot_icons/bell.jpg",
  "/static/slot_icons/cherry.jpg",
  "/static/slot_icons/diamond.jpg",
  "/static/slot_icons/heart.jpg",
  "/static/slot_icons/horseshoe.jpg",
  "/static/slot_icons/lemon.jpg",
  "/static/slot_icons/seven.jpg",
  "/static/slot_icons/watermelon.jpg",
];

let spinCost = 1; // Define the cost per spin

// Initiate reels function
function InitializeReels() {
  reels.forEach((reel) => {
    reel.innerHTML = `<img src="${images[7]}" alt="default" />`;
  });
}

// Function to spin
function spinReel(reel, duration) {
  let index = Math.floor(Math.random() * images.length);

  return new Promise((resolve) => {
    let startTime = Date.now();
    const interval = 100;

    const spin = setInterval(() => {
      index = (index + 1) % images.length;
      reel.innerHTML = `<img src="${images[index]}" alt="${images[index]}"/>`;

      if (Date.now() - startTime >= duration) {
        clearInterval(spin);
        resolve(images[index]);
      }
    }, interval);
  });
}

// Update Users cash, newCash = User's NEW CASH BALANCE
function updateCash(newCash) {
  // Send updated cash to backend
  return fetch("/update_cash", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      new_cash: newCash,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log(`Cash updated successfully: ${data.cash}`);
      } else {
        console.error(`Failed to update cash: ${data.error}`);
      }
    })
    .catch((error) => console.error("Error updating cash:", error));
}

// Calculate the payout
function checkResult(results) {
  let payout = 0;

  // Count matching symbols
  const symbolCount = {};
  results.forEach((symbol) => {
    symbolCount[symbol] = (symbolCount[symbol] || 0) + 1;
  });

  const allSymbols = Object.keys(symbolCount);

  // 3 Matching Symbols
  if (allSymbols.length === 1) {
    if (
      results[0] === images[7] ||
      results[0] === images[0] ||
      results[0] === images[3] ||
      results[0] === images[5]
    ) {
      // 7's, Bars, Diamonds, Horseshoe: 500x payout
      payout = 500;
    } else {
      // Other 3 matching symbols: 50x payout
      payout = 50;
    }
  }

  // 2 Matching Symbols Logic
  if (allSymbols.length === 2) {
    const matchedSymbol = results.find((symbol) => symbolCount[symbol] === 2);

    if (
      matchedSymbol === images[7] || // Sevens
      matchedSymbol === images[0] || // Bars
      matchedSymbol === images[3] || // Diamonds
      matchedSymbol === images[5] // Horseshoe
    ) {
      // 2 Matching (7's, Bars, Diamonds, Horseshoe): 10x payout
      payout = 10;
    } else {
      // Other 2 matching: 2x payout
      payout = 2;
    }
  }

  // Update message based on results
  if (payout > 0) {
    slots_message.textContent = `Against all odds, YOU WIN ${payout}x!`;
    slotMachine.classList.add("win");
  } else {
    slots_message.textContent =
      "Just remember, 100% of gamblers quit before they win big.";
    slotMachine.classList.add("loss");
  }
  return { payout };
}

// Starts the game
async function startGame() {
  slots_message.textContent = "";
  handleButton.disabled = true;

  // Reset any previous effects
  slotMachine.classList.remove("loss", "win");

  // Deduct spin cost from current cash
  const currentCash = parseInt(
    document
      .getElementById("current-cash")
      .textContent.replace("Your Cash: $", "")
      .trim()
  );

  const newCash = currentCash - spinCost; // Deduct the cost of the spin
  console.log(`Deducted spin cost. New Cash: $${newCash}`);

  await updateCash(newCash);

  // Update cash on the frontend
  const cashElement = document.getElementById("current-cash");
  cashElement.textContent = `Your Cash: $${newCash}`;

  // Spin the machine
  InitializeReels();

  const results = await Promise.all([
    spinReel(reels[0], 2000),
    spinReel(reels[1], 3000),
    spinReel(reels[2], 4000),
  ]);

  handleButton.disabled = false;

  // Calculate payout
  const { payout } = checkResult(results);

  // Send payout to the backend to update game stats
  const response = await fetch("/slots", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      payout, // The payout multiplier
    }),
  });

  // If everything went well...
  if (response.ok) {
    const data = await response.json();

    // Update the user's cash on the page
    const cashElement = document.getElementById("current-cash");
    cashElement.textContent = `Your Cash: $${data.current_cash}`;

    // Update spin cost dynamically as 1% of current cash
    spinCost = Math.max(1, Math.floor(data.current_cash * 0.01)); // 1% of current cash, with a minimum of $1
    const spinCostElement = document.getElementById("spin-cost");
    spinCostElement.textContent = `Cost Per Spin: $${spinCost}`;
  } else {
    console.error("Error in processing payout.");
  }
}

// Call function
InitializeReels();
handleButton.addEventListener("click", startGame);
