import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/card';
import { AlertCircle, Info, HelpCircle, Award } from 'lucide-react';

// Card suits and values
const SUITS = ['espadas', 'bastos', 'oros', 'copas'];
const CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12];

// Card ranking (highest to lowest)
const CARD_RANKING = [
  { suit: 'espadas', value: 1 }, // Ace of Swords
  { suit: 'bastos', value: 1 },  // Ace of Clubs
  { suit: 'espadas', value: 7 }, // Seven of Swords
  { suit: 'oros', value: 7 },    // Seven of Gold
  // All 3s
  { suit: 'espadas', value: 3 }, { suit: 'bastos', value: 3 },
  { suit: 'oros', value: 3 }, { suit: 'copas', value: 3 },
  // All 2s
  { suit: 'espadas', value: 2 }, { suit: 'bastos', value: 2 },
  { suit: 'oros', value: 2 }, { suit: 'copas', value: 2 },
  // Remaining Aces
  { suit: 'oros', value: 1 }, { suit: 'copas', value: 1 },
  // All Kings (12)
  { suit: 'espadas', value: 12 }, { suit: 'bastos', value: 12 },
  { suit: 'oros', value: 12 }, { suit: 'copas', value: 12 },
  // All Knights (11)
  { suit: 'espadas', value: 11 }, { suit: 'bastos', value: 11 },
  { suit: 'oros', value: 11 }, { suit: 'copas', value: 11 },
  // All Jacks (10)
  { suit: 'espadas', value: 10 }, { suit: 'bastos', value: 10 },
  { suit: 'oros', value: 10 }, { suit: 'copas', value: 10 },
  // Remaining 7s
  { suit: 'copas', value: 7 }, { suit: 'bastos', value: 7 },
  // All 6s
  { suit: 'espadas', value: 6 }, { suit: 'bastos', value: 6 },
  { suit: 'oros', value: 6 }, { suit: 'copas', value: 6 },
  // All 5s
  { suit: 'espadas', value: 5 }, { suit: 'bastos', value: 5 },
  { suit: 'oros', value: 5 }, { suit: 'copas', value: 5 },
  // All 4s
  { suit: 'espadas', value: 4 }, { suit: 'bastos', value: 4 },
  { suit: 'oros', value: 4 }, { suit: 'copas', value: 4 },
];

const SPECIAL_CARDS = {
  'espadas1': 'Ace of Swords (Highest card)',
  'bastos1': 'Ace of Clubs (2nd highest)',
  'espadas7': 'Seven of Swords (3rd highest)',
  'oros7': 'Seven of Gold (4th highest)',
};

// Suit emojis/symbols
const SUIT_SYMBOLS = {
  'espadas': '♠️',
  'bastos': '♣️',
  'oros': '🔶',
  'copas': '♥️'
};

// Spanish names for card values
const SPANISH_NAMES = {
  1: 'As',
  2: 'Dos',
  3: 'Tres',
  4: 'Cuatro',
  5: 'Cinco',
  6: 'Seis',
  7: 'Siete',
  10: 'Sota',
  11: 'Caballo',
  12: 'Rey'
};

// Spanish names for suits
const SUIT_NAMES = {
  'espadas': 'Espadas',
  'bastos': 'Bastos',
  'oros': 'Oros',
  'copas': 'Copas'
};

const createDeck = () => {
  const deck = [];
  SUITS.forEach(suit => {
    CARD_VALUES.forEach(value => {
      deck.push({ suit, value });
    });
  });
  return deck;
};

const shuffleDeck = (deck) => {
  let shuffled = [...deck];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};

const getCardRank = (card) => {
  return CARD_RANKING.findIndex(
    rankedCard => rankedCard.suit === card.suit && rankedCard.value === card.value
  );
};

const compareCards = (card1, card2) => {
  const rank1 = getCardRank(card1);
  const rank2 = getCardRank(card2);
  // Lower index means higher rank
  if (rank1 < rank2) return 1;  // card1 wins
  if (rank1 > rank2) return -1; // card2 wins
  return 0; // tie
};

const TrucoGame = () => {
  const [deck, setDeck] = useState([]);
  const [playerHand, setPlayerHand] = useState([]);
  const [opponentHand, setOpponentHand] = useState([]);
  const [playerScore, setPlayerScore] = useState(0);
  const [opponentScore, setOpponentScore] = useState(0);
  const [roundCards, setRoundCards] = useState({ player: null, opponent: null });
  const [rounds, setRounds] = useState([]);
  const [currentRound, setCurrentRound] = useState(1);
  const [gameState, setGameState] = useState('dealing'); // dealing, playing, roundEnd, gameEnd
  const [truco, setTruco] = useState(false);
  const [trucoValue, setTrucoValue] = useState(1); // 1, 2, 3, 4 (Truco, ReTruco, Vale Cuatro)
  const [message, setMessage] = useState('Welcome to Truco! I\'ll help you learn the game.');
  const [showRankings, setShowRankings] = useState(false);
  const [envido, setEnvido] = useState(false);
  const [envidoPoints, setEnvidoPoints] = useState({ player: 0, opponent: 0 });
  const [showAdvice, setShowAdvice] = useState(false);
  const [roundWins, setRoundWins] = useState({ player: 0, opponent: 0 });
  const [cardExplanation, setCardExplanation] = useState(null);

  // Initialize the game
  useEffect(() => {
    startNewHand();
  }, []);

  const startNewHand = () => {
    const newDeck = shuffleDeck(createDeck());
    
    // Deal 3 cards to each player
    const newPlayerHand = newDeck.slice(0, 3);
    const newOpponentHand = newDeck.slice(3, 6);
    
    setDeck(newDeck.slice(6));
    setPlayerHand(newPlayerHand);
    setOpponentHand(newOpponentHand);
    setRounds([]);
    setCurrentRound(1);
    setGameState('playing');
    setTruco(false);
    setTrucoValue(1);
    setEnvido(false);
    setRoundCards({ player: null, opponent: null });
    setRoundWins({ player: 0, opponent: 0 });
    setMessage("New hand dealt! You have the first play. Consider your cards carefully.");
    
    // Calculate envido points
    calculateEnvidoPoints(newPlayerHand, newOpponentHand);
  };

  const calculateEnvidoPoints = (playerCards, opponentCards) => {
    // Group cards by suit
    const playerSuits = {};
    playerCards.forEach(card => {
      if (!playerSuits[card.suit]) playerSuits[card.suit] = [];
      if (card.value <= 7) playerSuits[card.suit].push(card.value);
      else playerSuits[card.suit].push(0); // Face cards count as 0 for envido
    });
    
    const opponentSuits = {};
    opponentCards.forEach(card => {
      if (!opponentSuits[card.suit]) opponentSuits[card.suit] = [];
      if (card.value <= 7) opponentSuits[card.suit].push(card.value);
      else opponentSuits[card.suit].push(0); // Face cards count as 0 for envido
    });
    
    // Calculate highest envido for player
    let playerHighest = 0;
    Object.keys(playerSuits).forEach(suit => {
      if (playerSuits[suit].length >= 2) {
        // Sort in descending order
        const sortedValues = playerSuits[suit].sort((a, b) => b - a);
        const points = 20 + sortedValues[0] + sortedValues[1];
        playerHighest = Math.max(playerHighest, points);
      }
    });
    
    // If no pairs, use highest card
    if (playerHighest === 0) {
      playerCards.forEach(card => {
        if (card.value <= 7) playerHighest = Math.max(playerHighest, card.value);
      });
    }
    
    // Calculate highest envido for opponent
    let opponentHighest = 0;
    Object.keys(opponentSuits).forEach(suit => {
      if (opponentSuits[suit].length >= 2) {
        // Sort in descending order
        const sortedValues = opponentSuits[suit].sort((a, b) => b - a);
        const points = 20 + sortedValues[0] + sortedValues[1];
        opponentHighest = Math.max(opponentHighest, points);
      }
    });
    
    // If no pairs, use highest card
    if (opponentHighest === 0) {
      opponentCards.forEach(card => {
        if (card.value <= 7) opponentHighest = Math.max(opponentHighest, card.value);
      });
    }
    
    setEnvidoPoints({ player: playerHighest, opponent: opponentHighest });
  };

  const playCard = (card) => {
    if (gameState !== 'playing') return;
    
    // Remove card from player's hand
    const newPlayerHand = playerHand.filter(c => 
      !(c.suit === card.suit && c.value === card.value)
    );
    setPlayerHand(newPlayerHand);
    
    // Add card to round
    setRoundCards(prev => ({ ...prev, player: card }));
    setMessage(`You played ${SPANISH_NAMES[card.value]} de ${SUIT_NAMES[card.suit]}.`);
    
    // Computer plays after a short delay
    setTimeout(() => {
      playOpponentCard(newPlayerHand);
    }, 1000);
  };

  const playOpponentCard = (newPlayerHand) => {
    // Simple AI: play the weakest card that can win, or the weakest card if can't win
    let cardToPlay;
    const playerCard = roundCards.player;
    
    // Sort opponent's hand from weakest to strongest
    const sortedHand = [...opponentHand].sort((a, b) => {
      return getCardRank(a) - getCardRank(b);
    }).reverse(); // Reversed so higher indexes are weaker cards
    
    // Find the weakest card that can beat the player's card
    cardToPlay = sortedHand.find(card => compareCards(card, playerCard) > 0);
    
    // If can't win, play the weakest card
    if (!cardToPlay) {
      cardToPlay = sortedHand[sortedHand.length - 1];
    }
    
    // Remove card from opponent's hand
    const newOpponentHand = opponentHand.filter(c => 
      !(c.suit === cardToPlay.suit && c.value === cardToPlay.value)
    );
    setOpponentHand(newOpponentHand);
    
    // Add card to round
    setRoundCards(prev => ({ ...prev, opponent: cardToPlay }));
    
    setMessage(`Opponent played ${SPANISH_NAMES[cardToPlay.value]} de ${SUIT_NAMES[cardToPlay.suit]}.`);
    
    // Compare cards and determine round winner
    setTimeout(() => {
      evaluateRound(cardToPlay);
    }, 1000);
  };

  const evaluateRound = (opponentCard) => {
    const result = compareCards(roundCards.player, opponentCard);
    let newRoundWins = { ...roundWins };
    
    let roundWinner = '';
    if (result > 0) {
      roundWinner = 'player';
      newRoundWins.player += 1;
      setMessage('You won this round!');
    } else if (result < 0) {
      roundWinner = 'opponent';
      newRoundWins.opponent += 1;
      setMessage('Opponent won this round.');
    } else {
      roundWinner = 'tie';
      setMessage('This round is tied!');
    }
    
    // Record the round
    setRounds([...rounds, { 
      playerCard: roundCards.player, 
      opponentCard, 
      winner: roundWinner 
    }]);
    
    setRoundWins(newRoundWins);
    
    // Clear round cards after a delay
    setTimeout(() => {
      setRoundCards({ player: null, opponent: null });
      
      // Check if hand is over (i.e., someone won 2 rounds or all cards played)
      if (newRoundWins.player >= 2 || newRoundWins.opponent >= 2 || 
          (playerHand.length === 0 && opponentHand.length === 0) ||
          currentRound >= 3) {
        
        // Determine hand winner
        let handWinner = '';
        if (newRoundWins.player > newRoundWins.opponent) {
          handWinner = 'player';
          setPlayerScore(prevScore => prevScore + trucoValue);
          setMessage(`You won the hand! +${trucoValue} points`);
        } else if (newRoundWins.player < newRoundWins.opponent) {
          handWinner = 'opponent';
          setOpponentScore(prevScore => prevScore + trucoValue);
          setMessage(`Opponent won the hand. +${trucoValue} points for them.`);
        } else {
          // Ties are won by the player who won the first non-tied round
          const firstWin = rounds.find(round => round.winner !== 'tie');
          if (firstWin) {
            handWinner = firstWin.winner;
            if (handWinner === 'player') {
              setPlayerScore(prevScore => prevScore + trucoValue);
              setMessage(`Tied hand resolved by first win rule. You win! +${trucoValue} points`);
            } else {
              setOpponentScore(prevScore => prevScore + trucoValue);
              setMessage(`Tied hand resolved by first win rule. Opponent wins. +${trucoValue} points for them.`);
            }
          } else {
            setMessage("Completely tied hand! No points awarded.");
          }
        }
        
        setGameState('roundEnd');
        
        // Check for game end
        setTimeout(() => {
          if (playerScore >= 15 || opponentScore >= 15) {
            setGameState('gameEnd');
            if (playerScore >= 15) {
              setMessage("Congratulations! You won the game!");
            } else {
              setMessage("Game over! Opponent won the game.");
            }
          } else {
            setMessage("Click 'Next Hand' to continue.");
          }
        }, 1500);
      } else {
        // Continue to next round
        setCurrentRound(prevRound => prevRound + 1);
        setGameState('playing');
      }
    }, 1500);
  };

  const callTruco = () => {
    if (truco) {
      // Already called, increase the value
      const newValue = trucoValue + 1;
      if (newValue > 4) return; // Max is Vale Cuatro (4)
      
      setTrucoValue(newValue);
      
      // Name based on value
      let callName = '';
      if (newValue === 2) callName = 'Retruco';
      else if (newValue === 3) callName = 'Vale Tres';
      else if (newValue === 4) callName = 'Vale Cuatro';
      
      setMessage(`You called ${callName}! Opponent accepted, playing for ${newValue} points.`);
    } else {
      // First Truco call
      setTruco(true);
      setTrucoValue(2);
      setMessage("You called Truco! Opponent accepted, playing for 2 points.");
    }
  };

  const callEnvido = () => {
    if (envido) return; // Already called
    
    setEnvido(true);
    // Simple AI: opponent always accepts
    
    const playerPoints = envidoPoints.player;
    const opponentPoints = envidoPoints.opponent;
    
    setTimeout(() => {
      setMessage(`Envido called! Your points: ${playerPoints}, Opponent's points: ${opponentPoints}`);
      
      // Determine winner after a delay
      setTimeout(() => {
        if (playerPoints > opponentPoints) {
          setPlayerScore(prev => prev + 2);
          setMessage(`You win the Envido! +2 points (Your ${playerPoints} vs Opponent's ${opponentPoints})`);
        } else if (playerPoints < opponentPoints) {
          setOpponentScore(prev => prev + 2);
          setMessage(`Opponent wins the Envido. +2 points for them (Your ${playerPoints} vs Opponent's ${opponentPoints})`);
        } else {
          // In a tie, the dealer wins (we'll say opponent is dealer)
          setOpponentScore(prev => prev + 2);
          setMessage(`Envido tied at ${playerPoints} points. Dealer (opponent) wins. +2 points for them.`);
        }
      }, 2000);
    }, 1000);
  };

  const getCardAdvice = () => {
    if (playerHand.length === 0) return "You have no cards left to play.";
    
    // Sort hand by rank (worst to best)
    const sortedHand = [...playerHand].sort((a, b) => getCardRank(a) - getCardRank(b)).reverse();
    
    // First round strategy
    if (currentRound === 1) {
      // In first round, generally play a mid-strength card
      if (playerHand.length >= 2) {
        const midCard = sortedHand[1]; // Second worst card
        return `Consider playing your ${SPANISH_NAMES[midCard.value]} de ${SUIT_NAMES[midCard.suit]}. It's a mid-strength card, letting you save stronger cards for later rounds.`;
      }
    }
    
    // If winning the hand, play weakest
    if (roundWins.player > roundWins.opponent) {
      const weakestCard = sortedHand[sortedHand.length - 1];
      return `You're ahead in rounds! Consider playing your weakest card (${SPANISH_NAMES[weakestCard.value]} de ${SUIT_NAMES[weakestCard.suit]}) to preserve strength.`;
    }
    
    // If losing, play strongest
    if (roundWins.player < roundWins.opponent) {
      const strongestCard = sortedHand[0];
      return `You need this round! Consider playing your strongest card (${SPANISH_NAMES[strongestCard.value]} de ${SUIT_NAMES[strongestCard.suit]}).`;
    }
    
    // Default advice
    const bestCard = sortedHand[0];
    return `Your strongest card is ${SPANISH_NAMES[bestCard.value]} de ${SUIT_NAMES[bestCard.suit]}.`;
  };

  const showCardExplanation = (card) => {
    const rankIndex = getCardRank(card);
    let explanation = `${SPANISH_NAMES[card.value]} de ${SUIT_NAMES[card.suit]}`;
    
    // Check if it's a special card
    const cardKey = `${card.suit}${card.value}`;
    if (SPECIAL_CARDS[cardKey]) {
      explanation += ` - ${SPECIAL_CARDS[cardKey]}`;
    } else {
      // Generic ranking explanation
      explanation += ` - Ranked #${rankIndex + 1} out of 40 cards`;
      
      if (card.value === 3) {
        explanation += ". All 3s are strong cards in Truco.";
      } else if (card.value === 2) {
        explanation += ". 2s are strong middle-tier cards.";
      }
    }
    
    setCardExplanation(explanation);
    
    // Clear after 3 seconds
    setTimeout(() => {
      setCardExplanation(null);
    }, 3000);
  };

  const renderCard = (card, playable = false, isOpponent = false) => {
    if (!card) return null;
    
    const symbol = SUIT_SYMBOLS[card.suit];
    const spanishName = SPANISH_NAMES[card.value];
    
    // Calculate card value color
    let valueColor = 'text-black';
    if (card.suit === 'espadas' || card.suit === 'bastos') {
      valueColor = 'text-black';
    } else {
      valueColor = 'text-red-600';
    }
    
    let suitColor = 'bg-white';
    if (card.suit === 'espadas') suitColor = 'bg-gray-100'; 
    else if (card.suit === 'bastos') suitColor = 'bg-green-50';
    else if (card.suit === 'oros') suitColor = 'bg-yellow-50';
    else if (card.suit === 'copas') suitColor = 'bg-red-50';
    
    // For opponent cards, conditionally show back of card
    if (isOpponent && !roundCards.opponent) {
      return (
        <div className="w-20 h-32 bg-blue-500 rounded-lg flex items-center justify-center mx-1 border-2 border-blue-800 shadow">
          <div className="text-white text-xl font-bold">?</div>
        </div>
      );
    }
    
    return (
      <div 
        className={`w-20 h-32 ${suitColor} rounded-lg flex flex-col p-2 mx-1 border-2 border-gray-300 shadow ${playable ? 'cursor-pointer hover:border-blue-500 transform hover:-translate-y-2 transition-transform' : ''}`}
        onClick={() => {
          if (playable) {
            playCard(card);
          } else if (!isOpponent) {
            showCardExplanation(card);
          }
        }}
      >
        <div className={`flex justify-between ${valueColor}`}>
          <div className="text-lg font-bold">{card.value}</div>
          <div className="text-xl">{symbol}</div>
        </div>
        <div className="flex-grow flex items-center justify-center">
          <div className={`text-2xl ${valueColor}`}>{symbol}</div>
        </div>
        <div className={`flex justify-between ${valueColor}`}>
          <div className="text-xl">{symbol}</div>
          <div className="text-lg font-bold">{card.value}</div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col min-h-screen bg-green-900 text-white p-4">
      <h1 className="text-3xl font-bold text-center mb-4">Argentinian Truco</h1>
      
      {/* Score and game info */}
      <div className="flex justify-between mb-4">
        <div className="text-xl">
          You: {playerScore} points
        </div>
        <div className="text-center">
          {truco && <span className="px-2 py-1 bg-red-600 rounded-lg">Truco {trucoValue} pts</span>}
          {envido && <span className="ml-2 px-2 py-1 bg-blue-600 rounded-lg">Envido</span>}
        </div>
        <div className="text-xl">
          Opponent: {opponentScore} points
        </div>
      </div>
      
      {/* Round wins indicator */}
      <div className="flex justify-center mb-4">
        <div className="flex space-x-4">
          <div>
            Round wins - You: {roundWins.player} | Opponent: {roundWins.opponent}
          </div>
          <div>
            Round: {currentRound}/3
          </div>
        </div>
      </div>
      
      {/* Message area */}
      <div className="bg-green-800 p-4 mb-4 rounded-lg text-center min-h-12">
        {message}
        {cardExplanation && (
          <div className="mt-2 bg-yellow-800 p-2 rounded-lg">
            {cardExplanation}
          </div>
        )}
      </div>
      
      {/* Opponent's hand */}
      <div className="mb-8">
        <h2 className="text-xl mb-2">Opponent's Hand:</h2>
        <div className="flex justify-center">
          {opponentHand.map((card, index) => (
            <div key={index}>
              {renderCard(card, false, true)}
            </div>
          ))}
        </div>
      </div>
      
      {/* Playing area */}
      <div className="flex justify-center mb-8 min-h-40">
        <div className="flex space-x-16 items-center">
          <div>
            <p className="text-center mb-2">Opponent</p>
            {roundCards.opponent ? renderCard(roundCards.opponent) : (
              <div className="w-20 h-32 border-2 border-dashed border-gray-500 rounded-lg flex items-center justify-center">
                <span className="text-gray-400">Card</span>
              </div>
            )}
          </div>
          <div>
            <p className="text-center mb-2">You</p>
            {roundCards.player ? renderCard(roundCards.player) : (
              <div className="w-20 h-32 border-2 border-dashed border-gray-500 rounded-lg flex items-center justify-center">
                <span className="text-gray-400">Play a card</span>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Player's hand */}
      <div>
        <h2 className="text-xl mb-2">Your Hand:</h2>
        <div className="flex justify-center mb-4">
          {playerHand.map((card, index) => (
            <div key={index}>
              {renderCard(card, gameState === 'playing' && roundCards.player === null)}
            </div>
          ))}
        </div>
      </div>
      
      {/* Game controls */}
      <div className="flex justify-center space-x-4 mt-4">
        {gameState === 'playing' && !roundCards.player && (
          <>
            <button 
              className="px-4 py-2 bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50"
              onClick={callTruco}
              disabled={trucoValue >= 4}
            >
              {!truco ? 'Call Truco' : trucoValue === 2 ? 'Call ReTruco' : trucoValue === 3 ? 'Call Vale Tres' : 'Call Vale Cuatro'}
            </button>
            
            <button 
              className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
              onClick={callEnvido}
              disabled={envido || currentRound > 1}
            >
              Call Envido
            </button>
            
            <button 
              className="px-4 py-2 bg-yellow-600 rounded-lg hover:bg-yellow-700"
              onClick={() => setShowAdvice(!showAdvice)}
            >
              {showAdvice ? 'Hide Advice' : 'Get Advice'}
            </button>
          </>
        )}
        
        {gameState === 'roundEnd' && (
          <button 
            className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700"
            onClick={startNewHand}
          >
            Next Hand
          </button>
        )}
        
        {gameState === 'gameEnd' && (
          <button 
            className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700"
            onClick={() => {
              setPlayerScore(0);
              setOpponentScore(0);
              startNewHand();
            }}
          >
            New Game
          </button>
        )}
      </div>
      
      {/* Advice area */}
      {showAdvice && (
        <div className="mt-4 bg-yellow-800 p-4 rounded-lg">
          <h3 className="font-bold flex items-center">
            <HelpCircle className="mr-2" size={20} />
            Advice:
          </h3>
          <p>{getCardAdvice()}</p>
        </div>
      )}
      
      {/* Card ranking info */}
      <div className="mt-8">
        <button 
          className="w-full px-4 py-2 bg-blue-800 rounded-lg hover:bg-blue-900 flex items-center justify-center"
          onClick={() => setShowRankings(!showRankings)}
        >
          <Info className="mr-2" size={20} />
          {showRankings ? 'Hide Card Rankings' : 'Show Card Rankings'}
        </button>
        
        {showRankings && (
          <div className="mt-4 bg-gray-800 p-4 rounded-lg">
            <h3 className="font-bold mb-2">Card Rankings in Truco (Highest to Lowest):</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              <div>
                <p className="font-semibold">Top Cards:</p>
                <ol className="list-decimal list-inside">
                  <li>Ace of Swords (1 de Espadas)</li>
                  <li>Ace of Clubs (1 de Bastos)</li>
                  <li>Seven of Swords (7 de Espadas)</li>
                  <li>Seven of Gold (7 de Oros)</li>
                  <li>All Threes (3s)</li>
                  <li>All Twos (2s)</li>
                  <li>Ace of Gold (1 de Oros)</li>
                  <li>Ace of Cups (1 de Copas)</li>
                </ol>
              </div>
              <div>
                <p className="font-semibold">Lower Cards:</p>
                <ol className="list-decimal list-inside" start="9">
                  <li>All Kings (12s)</li>
                  <li>All Knights (11s)</li>
                  <li>All Jacks (10s)</li>
                  <li>Sevens of Cups and Clubs</li>
                  <li>All Sixes (6s)</li>
                  <li>All Fives (5s)</li>
                  <li>All Fours (4s)</li>
                </ol>
              </div>
            </div>
            <div className="mt-4">
              <p className="font-semibold">Key Game Terms:</p>
              <ul className="list-disc list-inside">
                <li><span className="font-bold">Truco:</span> Raises stakes to 2 points</li>
                <li><span className="font-bold">Retruco:</span> Raises stakes to 3 points</li>
                <li><span className="font-bold">Vale Cuatro:</span> Raises stakes to 4 points</li>
                <li><span className="font-bold">Envido:</span> Side bet worth 2 points based on same-suit card values</li>
              </ul>
            </div>
            <div className="mt-4">
              <p className="font-semibold">For 4 or 6 player games:</p>
              <ul className="list-disc list-inside">
                <li>Players form teams of 2 or 3</li>
                <li>Players take turns in sequence</li>
                <li>Team members cannot communicate about their cards</li>
                <li>Only one player per team can respond to Truco/Envido calls</li>
                <li>First team to reach 15 or 30 points wins</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TrucoGame;
