extends Control
var score = 0

@onready var label_4 = $Player/ZhuangTai/TextureRect/Label4





# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func add_point():
	score += 1
	label_4.text = "X"+str(score)
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
