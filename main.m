//
//  main.m
//  文件的读取与操作
//
//  Created by HZDL-PC on 16/8/28.
//  Copyright © 2016年 HZDL-PC. All rights reserved.
//

#import <Foundation/Foundation.h>


NSString *  stringfuctionDL(NSString *thing, NSString *sting1, NSString *string2);

NSString * stringfunctionDL(NSString *thing, NSString *sting1, NSString *string2){
    
    
    NSRange range = NSMakeRange(0, 0);
    NSRange range1 = NSMakeRange(0, 0);
    range = [thing rangeOfString:sting1];
    range1 = [thing rangeOfString:string2];
    
    if (range.length == 0 || range1.length == 0) {
        
        return @"null";
    }
    
    NSString *sting3 = [thing substringWithRange:NSMakeRange(range.location + range.length, range1.location  - range.location - range.length)];
    
    
    
    return sting3;
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {

        
        NSString *Filepath = @"/Users/HZDL-PC/Downloads/us.xml";
        NSString *finFilepath = @"/Users/HZDL-PC/Desktop/enclothing.json";
        NSString *finFilepath2 = @"/Users/HZDL-PC/Desktop/DLData.plist";
        
        NSFileManager *fileManager = [NSFileManager defaultManager];
        [fileManager createFileAtPath:finFilepath contents:nil attributes:nil];
        [fileManager createFileAtPath:finFilepath2 contents:nil attributes:nil];
        NSFileHandle *oriFile = [NSFileHandle fileHandleForReadingAtPath:Filepath];
        NSFileHandle *finFile = [NSFileHandle fileHandleForWritingAtPath:finFilepath];
        NSDictionary *oriAttr = [fileManager attributesOfItemAtPath:Filepath error:nil];
        NSNumber *fileSize0 = [oriAttr objectForKey:NSFileSize];
        NSInteger fileSize = [fileSize0 longValue];
        NSInteger fileReadSize = 0;
        [finFile writeData:[@"[" dataUsingEncoding:NSUTF8StringEncoding]];
        BOOL isEnd = YES;
        
        while (isEnd) {
            
            NSInteger sublength = fileSize - fileReadSize;
            NSData *data = nil;
            NSInteger i = 0;
            
            if (sublength < 2000) {
                isEnd = NO;
                
                data = [oriFile readDataToEndOfFile];
            } else {
                
                data = [oriFile readDataOfLength:6000];
                
                NSString *string = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
                
                NSArray *arr = [string componentsSeparatedByString:@"</entry>"];
                NSString *string2 = arr[0];
//                NSLog(@"%@", string2);
//                NSLog(@"%li", range.location);
//                NSLog(@"%@", string);
                
                if (string2.length > 1000) {
                    
                    NSMutableDictionary *dic = [NSMutableDictionary dictionary];
                    
                    
                    [dic setObject:stringfunctionDL(string2, @"<g:id>", @"</g:id>") forKey:@"id"];
                    [dic setObject:stringfunctionDL(string2, @"<g:mpn>", @"</g:mpn>") forKey:@"mpn"];
                    [dic setObject:stringfunctionDL(string2, @"<g:color>", @"</g:color>") forKey:@"color"];
                    [dic setObject:stringfunctionDL(string2, @"<g:title>", @"</g:title>") forKey:@"title"];
                    [dic setObject:stringfunctionDL(string2, @"<g:price>", @"</g:price>") forKey:@"price"];
                    [dic setObject:stringfunctionDL(string2, @"<g:availability>", @"</g:availability>") forKey:@"availability"];
                    [dic setObject:stringfunctionDL(string2, @"<g:brand>", @"</g:brand>") forKey:@"brand"];
                    [dic setObject: stringfunctionDL(string2, @"<g:link>", @"</g:link>") forKey:@"link"];
                    [dic setObject: stringfunctionDL(string2, @"<g:custom_label_0>", @"</g:custom_label_0>") forKey:@"custom_label_0"];
                
                    [dic setObject:stringfunctionDL(string2, @"<g:condition>", @"</g:condition>") forKey:@"condition"];
                   [dic setObject:stringfunctionDL(string, @"<g:description>", @"</g:description>") forKey:@"description"];
                    [dic setObject:stringfunctionDL(string2, @"<g:image_link>", @"</g:image_link>") forKey:@"image_link"];
                    [dic setObject:stringfunctionDL(string2, @"<g:additional_image_link>", @"</g:additional_image_link>") forKey:@"additional_image_link"];
                    
//                    NSString *ob = [NSString stringWithFormat:@"%@,", dic];
//                    data = [NSJSONSerialization dataWithJSONObject:ob options:0 error:nil];
                    data = [NSJSONSerialization dataWithJSONObject:dic options:NSJSONWritingPrettyPrinted error:nil];
//                    data = [ob dataUsingEncoding:NSUTF8StringEncoding];
                    
                    i = 1;
                }



                
                fileReadSize += string2.length + 8 ;
                [oriFile seekToFileOffset:fileReadSize];
                
                if (i == 1) {
                    [finFile writeData:data];
                    [finFile writeData:[@"," dataUsingEncoding:NSUTF8StringEncoding]];

//                    [finFile2 writeData:data];
                }
                
                
//
            }
            

        }
        [finFile seekToEndOfFile];
        [finFile writeData:[@"]" dataUsingEncoding:NSUTF8StringEncoding]];
        
        [oriFile closeFile];
        [finFile closeFile];
    }
    return 0;
}
