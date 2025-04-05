extends "res://assets/sprites/slime.gd"
@onready var save_slime = $"../Node/SaveSlime"


# Called when the node enters the scene tree for the first time.
func _process(delta):
	if ray_cast_right.is_colliding():
		direction = -1
		animated_sprite.flip_h = true
	if ray_cast_left.is_colliding():
		direction = 1
		animated_sprite.flip_h = false 
	position.x += direction * SPEED * delta
	
	


func _on_shouji_area_entered(area:Area2D):
	SPEED = 0
	sc1 += 1
	animation_player.play("shouji1")
	print(sc1,"血量")
	#queue_free()
	print("受击")
	if sc1 == 5:
		save_slime._sl1()
		queue_free()
	timer.start()
	
	
	
	


func _on_timer_timeout():
	SPEED = 60
	# Replace with function bo
