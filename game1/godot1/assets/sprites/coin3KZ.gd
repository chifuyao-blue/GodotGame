extends "res://assets/sprites/coin.gd"



# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_body_entered(_body):
	#get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
	label_4.add_point()
	label_4._co3()
	animation_player.play("pick_up")
