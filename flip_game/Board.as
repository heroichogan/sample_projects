class Board extends MovieClip { 

	private var NUM_PICTURES = 8 ;  // Must be >= 8
	private var NUM_CARDS_X = 4 ; 
	private var NUM_CARDS_Y = 4 ; 
	private var HIDE_DELAY = 2000 ; 
	private var CLICK_SOUND_LID = 'clickSoundLID' ; 
	private var GAME_OVER_SOUND_LID = 'gameOverSoundLID' ; 
	private var cardArray = [] ; 		
	private var firstCard:Card = null ; 
	private var cardCount:Number = 0 ; 
	private var interval:Number ; 
	private var sign:Sign ; 
	private var clickSound:Sound ; 
	private var gameOverSound:Sound ;

	
	public function Board() { 
		// Build cardArray	
		for( var i=0; i < this.NUM_CARDS_X; i++ ) {
			this.cardArray[i] = [] ; 
			for( var j=0; j < this.NUM_CARDS_Y; j++ ) {
				this.cardArray[i][j] = this['card' + i + j] ; 
			}
		}
		
		// Get reference to sign
		this.sign = this['signInstance'] ; 
		
		// Configure sound objects
		this.clickSound	= new Sound() ;  
		this.clickSound.attachSound( this.CLICK_SOUND_LID ) ; 		
		
		this.gameOverSound = new Sound() ; 
		this.gameOverSound.attachSound( this.GAME_OVER_SOUND_LID ) ; 
	}
	

	private function handleMove( chosenCard ):Void { 
	
		// Keep track of how many cards have been clicked (in brief period)
		this.cardCount ++ ; 

		// Decide if this is the first or second card
		if( this.cardCount == 1 ) { 
			// ...it's the first card
			this.firstCard = chosenCard ; 
			
			// Play sound			
			this.clickSound.start() ; 
			
		} else if( this.cardCount == 2 ) {
			// ...it's the second card
			var secondCard:Card = chosenCard ; 
			
			// Play sound
			this.clickSound.start() ; 			

			// Check for a match
			if( this.firstCard.pictureName == secondCard.pictureName ) {	
				// ...match
				this.firstCard.matched  = true ; 
				secondCard.matched = true ; 
				
				// Check for game over 
				if( this.isGameOver() )
					//...yes, game over
					this.quitGame() ; 
				else
					//...not game over, so handle the match
					this.handleMatch() ; 
			} else { 
				// ...no match
				this.interval = setInterval( this.hideCards, this.HIDE_DELAY, this, this.firstCard, secondCard ) ; 
				this.sign.moveToMessage( Sign.NO_MATCH ) ;  // NOTE:  This message resets in the animation, not in the code 
			}
			
			// Reset card ref & counter
			this.firstCard  = null ; 
			
		} else { 
			// Make sure at most two cards have been seleted		
			this.cardCount -- ; 
			throw new Error('Two cards already selected') ; 						
		}
		
		// Debug
		this.traceBoard() ; 
	}
	
	private function handleMatch():Void { 
		trace( '\nMade a match!' ) ; 
		this.sign.moveToMessage( Sign.MATCH ) ; 
		this.cardCount = 0 ; 
	}
	
	private function isGameOver():Boolean {
		try { 
			for( var i=0; i < this.NUM_CARDS_X; i++ )  
				for( var j=0; j < this.NUM_CARDS_Y; j++ )  
					if( !this.cardArray[i][j].matched ) 
						throw 'not over' ; 
		} catch( over ) {
			return false ; 
		}
		
		return true ; 
	}
	
	private function quitGame():Void { 
		trace( 'Game over!' ) ; 
		this.sign.moveToMessage( Sign.GAME_OVER ) ; 
		this.gameOverSound.start() ; 
	}
	
	
	private function hideCards( myThis, c1, c2 ):Void { 
		clearInterval( myThis.interval ) ; 
		c1.flip() ; 
		c2.flip() ; 
		myThis.cardCount = 0 ; 
		myThis.sign.moveToDefaultMessage() ; 				
		myThis.traceBoard() ; 
	}


	public function assignPictures():Void { 
		// Note:  can't call from constructor due to a Flash bug (Flash doesn't yet know the Cards are MovieClips)
		
		// From Flash help on random()
		function randRange(min:Number, max:Number):Number {
			return Math.round(Math.random()*(max-min))+min;
		}	
		
		// Build local cards array
		var cards = [] ; 
		for( var i=0; i < this.NUM_CARDS_X; i++ ) { 
			for( var j=0; j < this.NUM_CARDS_Y; j++ ) { 
				cards.push( this.cardArray[i][j] ) ; 
			} 
		} 
		
		// Build array of picture indexes
		var pix = [0,1,2,3,4,5,6,7] ;  // Must change if this.NUM_PICTURES changes
		
		// Match them up
		while( cards.length > 0 ) {
			var c1 = cards.splice( randRange(0,cards.length-1), 1 )[0] ; 
			var c2 = cards.splice( randRange(0,cards.length-1), 1 )[0] ; 
			var p = pix.splice( randRange(0,pix.length-1), 1 ) ; 
			
			c1.picture = c1.attachMovie( 'picture0' + p + '_LID', 'picture0' + p + '_instance1', c1.getNextHighestDepth() ) ; 
			c2.picture = c2.attachMovie( 'picture0' + p + '_LID', 'picture0' + p + '_instance2', c2.getNextHighestDepth() ); 
		}
	}
	
	
	
	private function traceBoard():Void { 
		trace('') ; 
		for( var j=0; j < this.NUM_CARDS_Y; j++ ) {
			var line = '' ; 
			for( var i=0; i < this.NUM_CARDS_X; i++ ) { 
				var x = this.cardArray[i][j] ; 
				if( x.matched ) 
					line = line + '*' + '\t' ; 
				else
					line = line + (this.cardArray[i][j].faceUp ? '1':'0') + '\t' ; 
			}
			trace(line) ; 
		}
	}
	
}