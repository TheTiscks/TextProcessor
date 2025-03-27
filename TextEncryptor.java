public class TextEncryptor {
    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Ошибка: Недостаточно аргументов");
            System.err.println("Использование: java TextEncryptor <режим> <текст>");
            System.err.println("Режимы: count, encrypt");
            System.exit(1); // код ошибки
        }

        String mode = args[0];
        String text = args[1];

        try {
            switch (mode) {
                case "count":
                    System.out.println(countWords(text));
                    break;
                case "encrypt":
                    System.out.println(encrypt(text));
                    break;
                default:
                    System.err.println("Ошибка: Неизвестный режим '" + mode + "'");
                    System.exit(1);
            }
        } catch (Exception e) {
            System.err.println("Ошибка обработки: " + e.getMessage());
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