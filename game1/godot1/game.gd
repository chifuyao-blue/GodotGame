extends Node2D

@onready var player = $Player
@onready var label_4 = $Player/ZhuangTai/TextureRect/Label4




var sc1 = 1
var changjing = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	changjing = 1
	_savechang1()
 # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	#if Input.is_action_pressed("ui_cancel"):
		#label_4._save()
		#player._save()
		#player._on_escape_pressed()
	

func _savechang1():
	var file = FileAccess.open("user://savechang1.tres",FileAccess.WRITE)
	file.store_var(sc1)
	file.close()
	
