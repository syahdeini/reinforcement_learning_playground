import matplotlib.pyplot as plt

files=["random_reward_file","q_agent_reward_file","q_agent_ench_reward_file","q_agent_add_behav_reward_file"]

for _file in files:
	epochs = []
	total_rewards = []
	means = []
	variances = []
	filename = _file
	f = open(filename,"r")
	for fline in f:
		epoch,mean,variance,total_reward = fline.strip().split("-")
		epochs.append(epoch)
		total_rewards.append(total_reward)
		means.append(mean)
		variances.append(variance)

	# print(epochs)
	fig = plt.figure()
	ax= fig.add_subplot(311)
	ax.plot(epochs,total_rewards)
	ax.set_title("learning curve")
	ax.set_xlabel('episode')
	ax.set_ylabel('total reward')
	ax= fig.add_subplot(312)
	ax.plot(epochs,means)
	ax.set_title("mean")
	ax.set_xlabel('episode')
	ax.set_ylabel('total reward')
	ax= fig.add_subplot(313)
	ax.plot(epochs,variances)
	ax.set_title("variance")
	ax.set_xlabel('episode')
	ax.set_ylabel('total reward')
	plt.tight_layout()
	plt.savefig(filename+".png")
	plt.clf()
