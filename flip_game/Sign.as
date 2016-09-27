class Sign extends MovieClip { 
	public static var DEFAULT = 0 ; 
	public static var NO_MATCH = 1 ; 
	public static var MATCH = 2 ; 
	public static var GAME_OVER = 3 ; 
	private var currentItem:Number ; 


	public function moveToMessage( item:Number ):Void { 
		this.gotoAndPlay( 'show' + item + 'Label') ; 
		this.currentItem = item ; 		
	}
	
	public function moveToDefaultMessage():Void { 
		this.gotoAndPlay( 'hide' + this.currentItem + 'Label') ; 
		this.currentItem = 0 ; 
	}
}