#include "lexical.h"

int main()
{

    string str;
    outFile.open("temp.txt",ios::out);
    Gram();
    outFile<<endl;
    //打印数据段
    outFile<<".section .data"<<endl;
    int max = 0;
    for(int t = 0;t < varlist.end;t++)
    {
        if(varlist.type[t] == le_string)
        {
            outFile<<"text"<<t<<": .ascii "<<"\""<<varlist.varList[t]<<"\\0"<<"\""<<endl;
        }
        else
        {
            if(varlist.addr[t] > max)
                max = varlist.addr[t];
        }
    }
    outFile.close();
    outFile.open("temp.txt");
    while(getline(outFile, str))
    {
        cout << str << endl;
    }
    cout<<endl<<endl<<endl;
    outFile.close();
    //输出符号表
    for(int t = 0;t < varlist.end;t++)
        cout<<t<<": "<<varlist.varList[t]<<"  "<<dec<<varlist.num[t]<<"  "<<dec<<varlist.addr[t]<<endl;
    return 0;
}
