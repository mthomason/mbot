import { describe, expect, it } from 'vitest';
import MessageBuilder from './MessageBuilder';

describe('MessageBuilder', () => {
	it('starts with a single empty block', () => {
		const builder = new MessageBuilder();

		expect(builder.getBlockCount()).toBe(1);
	});

	it('rejects non-string tokens', () => {
		const builder = new MessageBuilder();

		expect(() => builder.addToken(123 as unknown as string)).toThrow(TypeError);
	});

	it('adds multiple tokens without losing the instance context', () => {
		const builder = new MessageBuilder();

		builder.addTokens('Hello', ' ', 'World');

		expect(builder.getBlockHtml(0)).toContain('Hello World');
	});

	it('starts a new block on a double newline', () => {
		const builder = new MessageBuilder();

		builder.addTokens('First paragraph', '\n\n', 'Second paragraph');

		expect(builder.getBlockCount()).toBe(2);
		expect(builder.getBlockHtml(0)).toContain('First paragraph');
		expect(builder.getBlockHtml(1)).toContain('Second paragraph');
	});

	it('renders Markdown', () => {
		const builder = new MessageBuilder();

		builder.addTokens('**bold** and `code`');

		const html = builder.getBlockHtml(0);
		expect(html).toContain('<strong>bold</strong>');
		expect(html).toContain('<code>code</code>');
	});

	it('escapes raw HTML in the source', () => {
		const builder = new MessageBuilder();

		builder.addTokens('<script>alert("xss")</script>');

		expect(builder.getBlockHtml(0)).not.toContain('<script>');
	});

	it('validates block indexes', () => {
		const builder = new MessageBuilder();

		expect(() => builder.getBlockHtml(-1)).toThrow(RangeError);
		expect(() => builder.getBlockHtml(1)).toThrow(RangeError);
	});

	it('decorates every block in getHtml', () => {
		const builder = new MessageBuilder();
		builder.addTokens('One', '\n\n', 'Two');

		const html = builder.getHtml();
		expect(html.match(/message-block/g)).toHaveLength(2);
		expect(html).toContain('One');
		expect(html).toContain('Two');
	});
});
