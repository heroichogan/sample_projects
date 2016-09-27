class Card extends MovieClip { 
	private var board:MovieClip ; 
	private var _picture:MovieClip ; 
	private var _matched:Boolean = false ; 
	private var faceUp:Boolean = false ; 
	
	public function Card() {
		// Get board reference
		this.board = this._parent ;  
		
		// Set handler for mouse events
		this.onRelease = this.handleMove ; 
	}
	
	private function handleMove():Void { 
		if( !this.faceUp ) {
			try { 
				this.board.handleMove(this) ; 
				this.flip() ; 			
			} catch( e:Error ) { 
				// We skipped the flip(); nothing more to do
				trace( 'Got three clicks at once' ) ; 
			}
		}
	}
	
	private function flip():Void { 
		this.faceUp = !this.faceUp ; 
		if( this.faceUp ) 
			this.showFace() ; 
		else
			this.showBack() ; 
	}

	private function showFace():Void { 
		this.faceUp = true ; 
		this._picture.gotoAndPlay( "showPicture" ) ; 
	}
	
	private function showBack():Void { 
		this.faceUp = false ; 	
		this._picture.gotoAndPlay( "hidePicture" ) ; 		
	}
	
	public function set matched(matched:Boolean):Void { 
		this._matched = matched ; 
	}
	
	public function get matched():Boolean { 
		return this._matched ; 
	}
	
	public function set picture(picture:MovieClip):Void { 
		this._picture = picture ; 
	}
	
	public function get picture():MovieClip { 
		return this._picture ; 
	}
	
	public function get pictureName():String { 
		var x = this._picture._name ; 
		return x.slice( 0, x.length-1 ) ; 
	}
}