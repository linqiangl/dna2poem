package seven.test;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;

public class VocabTable implements Iterable<VocabWord> {
	private ArrayList<VocabWord> table;
	private HashMap<String, Integer> index;
	
	public VocabTable() {
		table = new ArrayList<>();
		index = new HashMap<>();
	}
	
	public int indexOf(String word) {
		if (word == null) return -1;
		Integer i = index.get(word);
		if (i == null) return -1;
		return (int)i;
	}
	
	public int add(String word) {
		int i = indexOf(word);
		if (i >= 0) {
			get(i).count ++;
			return i;
		}
		VocabWord v = new VocabWord();
		v.word = word;
		v.count = 1;
		i = table.size();
		table.add(v);
		index.put(word, i);
		return i;
	}
	
	public VocabWord get(int i) {
		return table.get(i);
	}
	
	public int size() {
		return table.size();
	}
	
	public void sort(long min_count) {
		Collections.sort(table);
		int i = 0;
		for (VocabWord v : table) {
			index.put(v.word, i);
			i ++;
		}
		reduce(min_count);
	}
	
	public void reduce(long min_count) {
		ArrayList<VocabWord> filter = new ArrayList<>();
		for (VocabWord v : table) {
			if (v.count >= min_count) {
				filter.add(v);
				index.put(v.word, filter.size() - 1);
			} else {
				index.remove(v.word);
			}
		}
		table = filter;
	}
	
	public void buildBinaryTree() {
		// assume: table is sorted
		int a, b, i, min1i, min2i, pos1, pos2, n;
		n = size();
		int[] point = new int[VocabWord.MAX_CODE_LENGTH];
		byte[] code = new byte[VocabWord.MAX_CODE_LENGTH];
		byte[] binary = new byte[n * 2 + 1];
		long[] count = new long[n * 2 + 1];
		int[] parent = new int[n * 2 + 1];
		
		i = 0; for (VocabWord v : table) {
			count[i] = v.count;
			i++;
		}
		for (; i < count.length; i++) {
			count[i] = Long.MAX_VALUE;
		}
		pos1 = n - 1;
		pos2 = n;
		for (a = 0; a < n; a++) {
			// First, find two smallest nodes 'min1, min2'
			if (pos1 >= 0) {
				if (count[pos1] < count[pos2]) {
					min1i = pos1;
					pos1--;
				} else {
					min1i = pos2;
					pos2++;
				}
			} else {
				min1i = pos2;
				pos2++;
			}
			if (pos1 >= 0) {
				if (count[pos1] < count[pos2]) {
					min2i = pos1;
					pos1--;
				} else {
					min2i = pos2;
					pos2++;
				}
			} else {
				min2i = pos2;
				pos2++;
			}
			count[n + a] = count[min1i] + count[min2i];
			parent[min1i] = n + a;
			parent[min2i] = n + a;
			binary[min2i] = 1;
		}
		
		for (a = 0; a < n; a++) {
			b = a;
			i = 0;
			while (true) {
				code[i] = binary[b];
				point[i] = b;
				i++;
				b = parent[b];
				if (b == n * 2 - 2)
					break;
			}
			VocabWord v = get(a);
			v.codelen = i;
			v.point[0] = n - 2;
			for (b = 0; b < i; b++) {
				v.code[i - b - 1] = code[b];
				v.point[i - b] = point[b] - n;
			}
		}
	}
	
	public void save(String filename) {
		try {
			PrintWriter writer = new PrintWriter(filename);
			for (VocabWord v : table) {
				writer.write(String.format("%s %d\n", v.word, v.count));
			}
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public void load(String filename) {
		try {
			BufferedReader reader = new BufferedReader(new FileReader(filename));
			String line;
			while ((line = reader.readLine()) != null) {
				if (line.length() == 0) continue;
				String[] values = line.split(" ");
				int i = add(values[0]);
				VocabWord v = get(i);
				v.count = Long.parseLong(values[1]);
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public long count(String filename, long min_reduce, long min_count) {
		try {
			long train_words = 0;
			add("</s>");
			FileInputStream reader = new FileInputStream(filename);
			Tokenizer tokenizer = new Tokenizer(reader);
			String word = null;
			while ((word = tokenizer.next()) != null) {
				train_words ++;
				add(word);
				// TODO: large amount of words, then reduce(min_reduce); min_reduce++;
			}
			reader.close();
			sort(min_count);
			return train_words;
		} catch (Exception e) {
			e.printStackTrace();
			return -1;
		}
	}

	@Override
	public Iterator<VocabWord> iterator() {
		return table.iterator();
	}
}
