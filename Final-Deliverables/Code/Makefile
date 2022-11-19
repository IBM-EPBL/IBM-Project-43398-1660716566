container:
	# sudo docker build -t pda .
	# sudo ibmcloud login -u 713319EC074@smartinternz.com -p spr12345spr_A
	# sudo ibmcloud cr login
	# sudo ibmcloud cr image-rm au.icr.io/value/pda:latest
	sleep 20
	sudo docker tag pda au.icr.io/value/pda
	sudo docker push au.icr.io/value/pda:latest

update-production:
	sudo make container
	sudo ibmcloud ks cluster config -c cdke5sgf0fuqubtfjpl0
	sleep 5
	sudo kubectl rollout restart -n default deployment plasmadonor

