intents = {
		"welcome":{
			"bot":["Hi there, Welcome to Insent.ai. How can I help you today?"],
			"answers":[
				{
					"answer":"Know more about Insent.ai",
					"nextId":"insent_description"
				},
				{
					"answer":"Keep me posted. I want to subscribe",
					"nextId":"subscribe_insent"
				},
				{
					"answer":"Talk to Insent.ai team",
					"nextId":"connect_insent_team"
				},
				{
					"answer": "Just Browsing",
					"nextId":"browsing"
				}
			]
		},

		"insent_description":{
			"bot":["Awesome. Insent.ai is a conversational marketing platform that connects B2B sellers to buyers when they are researching on products.",
				"When the B2B potential buyers are on third-party content websites and researching about their product buy, Insent.ai, which is already integrated with several publishers, will engage with the reader.",
				"Insentbot assesses the Intent, gathers the consent and capture the buyer as a lead. These leads will be passed on to the relevant buyers.",
				"You are experiencing the Insentbot interaction like a reader would experience it on a third party website.",
				"Would you like to be updated about the industry by subscribing to us?"
			],
			"answers":[
				{
					"answer":"Yes, I want to subscribe",
					"nextId":"subscribe_insent"
				},
				{
					"answer":"No, I am good for now",
					"nextId":"good_for_now"
				}
			]

		},

		"subscribe_insent":{
			"bot":["What is a good email for you?"],
			"answers":[
				{
					"nextId":"convo_end"
				}
			]
		},
		"company":{
			"bot":[ "I like to personalize more by knowing your company name."],
			"answers":[
				{
					"nextId":"convo_end"
				}
			]
		},

		"connect_insent_team":{
			"bot":["Let me try to see if the team is available at the moment", "Looks like they are busy scaling insent. But I know they love to speak with interested folks", "Do u want to subscribe for now ?"],

			"answers":[
				{
					"answer":"Yes, I want to subscribe",
					"nextId":"subscribe_insent"
				},
				{
					"answer":"No, I am good for now",
					"nextId":"good_for_now"
				}
			]

		},


		"browsing":{
			"bot":["You know where to find me. "],

			"answers":[
			{
				"nextId":"convo_end"
			}
			]

		},

		"good_for_now":{
			"bot":["Alright. If you need anything, let me know by typing /start"],

			"answers":[
			{
				"nextId":"convo_end"
			}
			]

		}
	}
