import java.io.FileNotFoundException;

public class Interpreter
{

	public static void main(String[] args)
	{
		try
		{
			Parser p = new Parser ("test4.lua");
			Program prog = p.parse();
			prog.execute();
		}
		catch (ParserException e)
		{
			System.out.println (e.getMessage());
		}
		catch (LexicalException e)
		{
			System.out.println (e.getMessage());
		}
		catch (IllegalArgumentException e)
		{
			System.out.println (e.getMessage());
		}
		catch (FileNotFoundException e)
		{
			System.out.println ("source file is not found");
		}
		catch (Exception e)
		{
			System.out.println ("unknown error occurred - terminating");
		}
	}

}
