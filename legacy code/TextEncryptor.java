public class TextEncryptor {
    public static void main(String[] args) {
        try {
            if (args.length < 2) {
                System.err.println("Ошибка: Недостаточно аргументов");
                System.err.println("Использование: java TextEncryptor <режим> <текст>");
                System.exit(1);
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
                    System.err.println("Неизвестный режим: " + mode);
                    System.exit(1);
            }
        } catch (Exception e) {
            System.err.println("Ошибка: " + e.getMessage());
            System.exit(1);
        }
    }

    private static int countWords(String text) {
        if (text == null || text.trim().isEmpty()) return 0;
        return text.trim().split("\\s+").length;
    }

    private static String encrypt(String text) {
        return new StringBuilder(text).reverse().toString();
    }
}