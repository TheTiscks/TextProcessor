public class TextEncryptor {
    public static void main(String[] args) {
        String text = args[0];
        System.out.println(new StringBuilder(text).reverse().toString()); // Простое реверс-шифрование для примера
    }
}