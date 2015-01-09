classmap_core:
	php --define include_path=../library classmap_generator.php -w -l ../library -o ../library/class_map.php
	php --define include_path=../library classmap_generator.php -w -l ../application -o ../application/class_map.php

classmap_conf:
	php --define include_path=../library classmap_generator.php -w -l ../configuration -o ../configuration/class_map.php

classmap_all: classmap_conf classmap_core

