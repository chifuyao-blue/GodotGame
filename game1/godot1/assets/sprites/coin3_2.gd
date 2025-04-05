extends "res://assets/sprites/coin.gd"

@onready var label_7 = $"../../Player/CanvasLayer/TextureRect/Label7"

func _on_body_entered(_body):
	#get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	label_7.add_point()
	label_7._co2()
	animation_player.play("pick_up")

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
