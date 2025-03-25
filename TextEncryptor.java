public class TextEncryptor {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Использование: <режим> <текст>");
            System.out.println("Режимы: count, encrypt");
            return;
        }

        String mode = args[0];
        String text = args[1];

        switch (mode) {
            case "count":
                System.out.println(countWords(text));
                break;
            case "encrypt":
                System.out.println(encrypt(text));
                break;
            default:
                System.out.println("Неизвестный режим");
        }
    }

    private static int countWords(String text) {
        if (text == null || text.isEmpty()) return 0;
        return text.trim().split("\\s+").length;
    }

    private static String encrypt(String text) {
        return new StringBuilder(text).reverse().toString();
    }
}