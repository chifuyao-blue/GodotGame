extends "res://assets/sprites/coin.gd"

@onready var label_6 = $"../../Player3/CanvasLayer/TextureRect/Label6"

func _on_body_entered(_body):
	#get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	label_6.add_point()
	label_6._co7()
	animation_player.play("pick_up")

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
