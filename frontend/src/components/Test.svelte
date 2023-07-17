<script>
	let count = 0;
	let message = "";

	// Built a string using concatenation
	function function1() {
		let s = "hello";
		for (let i = 0; i < 1e6; i++) {
			s += Math.floor(Math.random() * 10).toString();
		}
		return s;
	}

	// Built a string using an array
	function function2() {
		let sa = ["hello"];
		for (let i = 0; i < 1e6; i++) {
			sa.push(Math.floor(Math.random() * 10).toString());
		}
		return sa;
	}

	function handleClick() {
		let t0 = performance.now();
		let s0 = function1();

		let t1 = performance.now();
		let m = "Function 1 took " + (t1 - t0) + " milliseconds.";
		console.log(m);
		message = m;
	
		// Measure the time taken by function2
		t0 = performance.now();
		let s1 = function2();
		t1 = performance.now();
		m = "Function 2 took " + (t1 - t0) + " milliseconds.";
		console.log(m);
		message += "\n" + m;
	}


</script>

<button on:click={handleClick}>
	clicks: {count}
</button>
<div>
	{message}
</div>