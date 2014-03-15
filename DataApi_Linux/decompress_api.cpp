#define __int64 long long
extern "C" {  
	int decompressData(__int64 &iData, char *p)
	{
		int size = 1;
		int vol = 1;
		iData = 0;
		if((p[0]&0x03)==3) vol = 1000;
		else if((p[0]&0x03)==2) vol = 100;
		else if((p[0]&0x03)==1) vol = 10;
		else vol = 1;

		if((p[0]&0x70)==0 && (p[0]&0x0c)==0) iData = 0;
		else if((p[0]&0x0c)==0x04) iData = 1;
		else if((p[0]&0x0c)==0x08) iData = 2;
		else if((p[0]&0x0c)==0x0c) iData = 3;
		else 
		{
			switch(p[0]&0x70)
			{
			case 0x10:
				iData = p[1]&0xff;
				size = 2;
				break;
			case 0x20:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00);
				size = 3;
				break;
			case 0x30:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00) | ((p[3]<<16)&0xff0000);
				size = 4;
				break;
			case 0x40:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00) | ((p[3]<<16)&0xff0000) | ((p[4]<<24)&0xff000000);
				size = 5;
				break;
			case 0x50:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00) | ((p[3]<<16)&0xff0000) | ((p[4]<<24)&0xff000000) | (((__int64)(p[5]&0xff)<<32)&0xff00000000L);
				size = 6;
				break;
			case 0x60:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00) | ((p[3]<<16)&0xff0000) | ((p[4]<<24)&0xff000000) | (((__int64)(p[5]&0xff)<<32)&0xff00000000) | (((__int64)(p[6]&0xff)<<40)&0xff0000000000);
				size = 7;
				break;
			case 0x70:
				iData = (p[1]&0xff) | ((p[2]<<8)&0xff00) | ((p[3]<<16)&0xff0000) | ((p[4]<<24)&0xff000000) | (((__int64)(p[5]&0xff)<<32)&0xff00000000) | (((__int64)(p[6]&0xff)<<40)&0xff0000000000) | (((__int64)(p[7]&0xff)<<48)&0xff000000000000);
				size = 8;
				break;
			}
		}
		iData *= vol;
		if(p[0]&0x80)
		{
			iData *= -1;
		}
		return size;
	}
}