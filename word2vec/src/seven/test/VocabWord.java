package seven.test;

public class VocabWord implements Comparable<VocabWord> {
	public static final int MAX_CODE_LENGTH = 40;
	
	public String word;
	public long count;
	public byte[] code;
	public int codelen;
	public int[] point;
	
	public VocabWord() {
		code = new byte[MAX_CODE_LENGTH];
		point = new int[MAX_CODE_LENGTH];
	}
	
	@Override
	public int compareTo(VocabWord another) {
		if (another.count > count) {
			return 1;
		}
		if (another.count < count) {
			return -1;
		}
		return 0;
	}
}
