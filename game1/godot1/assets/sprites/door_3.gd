extends Area2D
@onready var animation_player = $Label/AnimationPlayer
@onready var timer = $Timer


func _on_body_entered(body):
	animation_player.play("tongguan1")
	timer.start()


func _on_timer_timeout():
	get_tree().change_scene_to_file("res://scenes/title_screen.tscn")
