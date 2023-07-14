"use strict"

/** 
 * ChatClient
 * @description
 * Manages chat responses from the server.
 * 
 * @class
 * @property {string[]} messages
 * @property {string} userChatPrompt
 * */
export default class ChatClient {
	messages: any[];
	userChatPrompt: string;
	constructor() {
		this.messages = [];
		this.userChatPrompt = "";
	}

	/**
	 * @description
	 * Post a message to the chat server.
	 * @returns {Promise<Response>}
	 * @throws {Error}
	 * @throws {TypeError}
	 * @throws {SyntaxError}
	 * @throws {ReferenceError}
	 * @throws {RangeError}
	 * 
	 * @example
	 * const chatClient = new ChatClient();
	 * chatClient.userChatPrompt = "Hello World";
	 * chatClient.postChatMessage();
	 */
	async postChatMessage(): Promise<Response> {
		if (!this.userChatPrompt) throw new Error("Message is empty");
		if (this.userChatPrompt.length === 0) throw new Error("Message is empty");

		try {
			const response = await fetch("http://localhost:8000/chat", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ message: this.userChatPrompt }),
			});
			return response;
		} catch (error) {
			console.error(error);
			throw error;
		}
	}
}
